<script lang="ts">
  import { createVirtualizer } from "@tanstack/svelte-virtual";
  import { get } from "svelte/store";
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

  // Create virtualizer with GENEROUS spacing to prevent overlap
  const virtualizerStore = $derived(
    scrollContainer
      ? createVirtualizer({
          count: displayMessages.length,
          getScrollElement: () => scrollContainer ?? null,
          estimateSize: (index) => {
            // Generous estimate to prevent overlap
            const message = displayMessages[index];
            const contentLength = message?.content?.length || 0;
            // Very conservative: 50 chars per line
            const charsPerLine = 50;
            const lines = Math.max(1, Math.ceil(contentLength / charsPerLine));
            // Generous line height + padding
            const textHeight = lines * 28;
            const basePadding = 80; // Avatar, author, timestamp, padding
            const extraGap = 32; // Big gap between messages
            return textHeight + basePadding + extraGap;
          },
          overscan: 3,
        })
      : null,
  );

  // Subscribe to store to get values
  let virtualItems = $state<{ index: number; start: number; size: number }[]>(
    [],
  );
  let totalSize = $state(0);

  $effect(() => {
    if (virtualizerStore) {
      const unsubscribe = virtualizerStore.subscribe((v) => {
        virtualItems = v.getVirtualItems();
        totalSize = v.getTotalSize();
      });
      return unsubscribe;
    }
  });

  // Scroll to bottom when new messages arrive
  $effect(() => {
    if (displayMessages.length > prevMessageCount && virtualizerStore) {
      prevMessageCount = displayMessages.length;
      // Small delay to ensure render is complete
      setTimeout(() => {
        const v = get(virtualizerStore);
        v.scrollToIndex(displayMessages.length - 1, {
          align: "end",
          behavior: "smooth",
        });
      }, 50);
    }
  });

  function handleScroll() {
    // Load more when scrolled near top (for older messages)
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

<section class="flex-1 overflow-hidden bg-gray-50 rounded-lg relative">
  {#if loading && messages.length === 0}
    <div class="flex items-center justify-center h-full">
      <p class="text-gray-500">Loading messages...</p>
    </div>
  {:else if messages.length === 0}
    <div class="flex items-center justify-center h-full">
      <p class="text-gray-500">
        No messages yet. Be the first caveman to grunt! 🍌
      </p>
    </div>
  {:else}
    <div
      bind:this={scrollContainer}
      onscroll={handleScroll}
      class="h-full overflow-y-auto"
    >
      <div style="height: {totalSize}px; width: 100%; position: relative;">
        {#each virtualItems as row (row.index)}
          <div
            data-index={row.index}
            style="position: absolute; top: 0; left: 0; width: 100%; transform: translateY({row.start}px);"
            class="px-4 pb-8"
          >
            <MessageItem message={displayMessages[row.index]} />
          </div>
        {/each}
      </div>
    </div>
    {#if loading}
      <div
        class="absolute top-2 left-1/2 -translate-x-1/2 bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-sm"
      >
        Loading older messages...
      </div>
    {/if}
  {/if}
</section>
