<script lang="ts">
  import { createVirtualizer } from "@tanstack/svelte-virtual";
  import MessageItem from "./MessageItem.svelte";
  import MessageLoading from "./MessageLoading.svelte";
  import { chatStore } from "$lib/stores/chat.svelte";
  import type { Message } from "$lib/types/chat";

  let {
    messages = [],
    loading = false,
    hasMore = false,
    onLoadMore,
  }: {
    messages: Message[];
    loading: boolean;
    hasMore: boolean;
    onLoadMore: () => void;
  } = $props();

  let scrollContainer = $state<HTMLDivElement>();
  let prevMessageCount = $state(0);
  let isLoadingOlder = $state(false);

  // Reversed messages for display (oldest at top, newest at bottom)
  const displayMessages = $derived([...messages].reverse());

  // 🦍 FORCE SCROLL TO BOTTOM - NO MERCY!
  function forceScrollToBottom() {
    if (!scrollContainer) return;
    
    // Direct manipulation - FORCE IT! 🍌
    scrollContainer.scrollTop = scrollContainer.scrollHeight;
    
    // Also use scrollTo for good measure
    scrollContainer.scrollTo({
      top: scrollContainer.scrollHeight,
      behavior: 'auto'
    });
  }

  // TanStack Virtual - FIXED: Proper spacing calculation! 🦍
  const virtualizer = $derived.by(() => {
    if (!scrollContainer) return null;
    
    return createVirtualizer<HTMLDivElement, HTMLDivElement>({
          count: displayMessages.length,
          getScrollElement: () => scrollContainer ?? null,
          estimateSize: (index) => {
            // Calculate based on ACTUAL lines including newlines!
            const message = displayMessages[index];
            if (!message) return 180;
            
            const content = message.content || '';
            if (content.length === 0) return 120;
            
            // Count ACTUAL lines with accurate wrapping!
            const lines = content.split('\n');
            let totalLines = 0;
            
            // Account for actual container width after padding
            // Message is max 50% width of container
            // Container ~1040px, 50% = 520px, minus padding (p-4 + pl-52) = ~452px for text
            const containerWidth = 450; // Conservative estimate for 50% messenger-style
            const avgCharWidth = 8.5; // Average character width in pixels
            const charsPerLine = Math.floor(containerWidth / avgCharWidth); // ~53 chars
            
            for (const line of lines) {
              if (line.length === 0) {
                totalLines += 1; // Empty line
              } else {
                // Count emojis - they take ~2x space
                const emojiCount = (line.match(/[\p{Emoji}\p{Emoji_Presentation}]/gu) || []).length;
                const effectiveLength = line.length + emojiCount; // Emojis count as 2 chars
                totalLines += Math.max(1, Math.ceil(effectiveLength / charsPerLine));
              }
            }
            
            totalLines = Math.max(1, totalLines);
            
            // Precise pixel breakdown with consistent safety margin:
            const avatarArea = 54;        // h-10 + gap + mb-3
            const lineHeight = 26;        // leading-relaxed
            const contentArea = totalLines * lineHeight;
            const cardPadding = 32;       // p-4 (16+16)
            const messageGap = 16;        // mb-4
            const borderWidth = 2;        // border (1+1)
            const consistentMargin = 8;   // Consistent safety for all messages
            
            return avatarArea + contentArea + cardPadding + messageGap + borderWidth + consistentMargin;
          },
          overscan: 5,
        });
  });

  // 🦍 SCROLL LOGIC - Keep chat at bottom!
  $effect(() => {
    const currentCount = displayMessages.length;

    // FIRST LOAD - Scroll to bottom!
    if (currentCount > 0 && prevMessageCount === 0) {
      prevMessageCount = currentCount;
      isLoadingOlder = false;
      
      forceScrollToBottom();
      setTimeout(() => forceScrollToBottom(), 100);
      return;
    }

    // NEW MESSAGE ARRIVED!
    if (currentCount > prevMessageCount) {
      // If loading older messages, just mark it
      if (loading) {
        isLoadingOlder = true;
      } else if (isLoadingOlder) {
        // Just finished loading older messages - DON'T scroll
        isLoadingOlder = false;
        prevMessageCount = currentCount;
        return;
      } else {
        // NEW MESSAGE from user or AI - Scroll to bottom! 🍌
        prevMessageCount = currentCount;
        
        // Two attempts: immediate + delayed for virtualizer
        forceScrollToBottom();
        setTimeout(() => forceScrollToBottom(), 100);
      }
    }
  });

  // 🦍 When AI starts generating, scroll to bottom!
  $effect(() => {
    if (chatStore.aiGenerating && scrollContainer) {
      forceScrollToBottom();
    }
  });

  // Handle scroll for infinite loading
  function handleScroll() {
    // Load older messages if scrolled to top
    if (
      scrollContainer &&
      scrollContainer.scrollTop < 100 &&
      hasMore &&
      !loading
    ) {
      isLoadingOlder = true;
      onLoadMore();
    }
  }
</script>

<style>
  /* Ensure proper box-sizing for accurate measurements */
  .virtual-item-wrapper {
    box-sizing: border-box;
  }
</style>

<section class="flex-1 overflow-hidden bg-muted/30 rounded-lg relative">
  {#if loading && messages.length === 0}
    <div class="flex items-center justify-center h-full px-4">
      <p class="text-muted-foreground text-sm md:text-base text-center">Loading messages...</p>
    </div>
  {:else if messages.length === 0}
    <div class="flex items-center justify-center h-full px-4">
      <p class="text-muted-foreground text-sm md:text-base text-center">
        No messages yet. Be the first caveman to grunt! 🍌
      </p>
    </div>
  {:else}
    <div
      bind:this={scrollContainer}
      onscroll={handleScroll}
      class="h-full overflow-y-auto px-2 md:px-4 py-4"
    >
      <div>
        {#if virtualizer}
          <!-- TanStack Virtual Container - OFFICIAL PATTERN! -->
          <div
            style="position: relative; height: {$virtualizer!.getTotalSize()}px; width: 100%;"
          >
            {#each $virtualizer!.getVirtualItems() as row (row.index)}
              <div
                class="virtual-item-wrapper"
                style="position: absolute; top: 0; left: 0; width: 100%; transform: translateY({row.start}px);"
                data-index={row.index}
              >
                <MessageItem message={displayMessages[row.index]} />
              </div>
            {/each}
          </div>
        {/if}
        <!-- AI Loading Indicator - appears below virtual items -->
        {#if chatStore.aiGenerating}
          <MessageLoading />
        {:else}
          <div style="display: none;">[aiGenerating: {chatStore.aiGenerating}]</div>
        {/if}
      </div>
    </div>
    {#if loading}
      <div
        class="absolute top-2 left-1/2 -translate-x-1/2 bg-primary/10 text-primary px-2 md:px-3 py-1 md:py-1.5 rounded-full text-xs md:text-sm font-medium border whitespace-nowrap"
      >
        Loading older messages...
      </div>
    {/if}
  {/if}
</section>
