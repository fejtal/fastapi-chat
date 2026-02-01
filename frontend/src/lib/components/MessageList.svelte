<script lang="ts">
  import { createVirtualizer } from "@tanstack/svelte-virtual";
  import MessageItem from "./MessageItem.svelte";
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

  // Reversed messages for display (oldest at top, newest at bottom)
  const displayMessages = $derived([...messages].reverse());

  // TanStack Virtual - FIXED: Proper spacing calculation! 🦍
  const virtualizer = $derived(
    scrollContainer
      ? createVirtualizer<HTMLDivElement, HTMLDivElement>({
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
            // Container is ~1040px, minus px-4 (32px), minus pl-[52px] = ~956px for text
            const containerWidth = 956;
            const avgCharWidth = 8.5; // Average character width in pixels
            const charsPerLine = Math.floor(containerWidth / avgCharWidth); // ~112 chars
            
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
            
            // Exact pixel breakdown:
            const avatarArea = 54;        // Measured
            const lineHeight = 26;        // leading-relaxed computed
            const contentArea = totalLines * lineHeight;
            const cardPadding = 32;       // p-4 
            const messageGap = 16;        // mb-4
            const borderWidth = 2;        // border
            
            return avatarArea + contentArea + cardPadding + messageGap + borderWidth;
          },
          overscan: 5,
        })
      : null,
  );

  // Auto-scroll to bottom when new messages arrive
  $effect(() => {
    if (displayMessages.length > prevMessageCount && virtualizer) {
      prevMessageCount = displayMessages.length;
      // Scroll to bottom
      setTimeout(() => {
        if (virtualizer) {
          virtualizer.subscribe((v) => {
            v.scrollToIndex(displayMessages.length - 1, {
              align: "end",
            });
          })();
        }
      }, 100);
    }
  });

  // Handle scroll for infinite loading
  function handleScroll() {
    if (
      scrollContainer &&
      scrollContainer.scrollTop < 100 &&
      hasMore &&
      !loading
    ) {
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
    <div class="flex items-center justify-center h-full">
      <p class="text-muted-foreground">Loading messages...</p>
    </div>
  {:else if messages.length === 0}
    <div class="flex items-center justify-center h-full">
      <p class="text-muted-foreground">
        No messages yet. Be the first caveman to grunt! 🍌
      </p>
    </div>
  {:else}
    <div
      bind:this={scrollContainer}
      onscroll={handleScroll}
      class="h-full overflow-y-auto px-4 py-4"
    >
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
    </div>
    {#if loading}
      <div
        class="absolute top-2 left-1/2 -translate-x-1/2 bg-primary/10 text-primary px-3 py-1.5 rounded-full text-sm font-medium border"
      >
        Loading older messages...
      </div>
    {/if}
  {/if}
</section>
