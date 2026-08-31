def fifo_page_replacement(pages, frames):
    memory = []
    hits = 0
    misses = 0

    for page in pages:
        if page in memory:
            hits += 1
        else:
            misses += 1

            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)

    return hits, misses


def lru_page_replacement(pages, frames):
    memory = []
    hits = 0
    misses = 0

    for page in pages:
        if page in memory:
            hits += 1
            memory.remove(page)
            memory.append(page)
        else:
            misses += 1

            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)

    return hits, misses


print("Memory Management - Page Replacement")
print("S123 Dhruv Yadav")

reference_string = list(map(int, input(
    "Enter page reference string (e.g. 1 2 3 1 4 2 5): "
).split()))

frames = int(input("Enter number of frames: "))

fifo_hits, fifo_misses = fifo_page_replacement(reference_string, frames)

lru_hits, lru_misses = lru_page_replacement(reference_string, frames)

total_pages = len(reference_string)

fifo_hit_ratio = fifo_hits / total_pages
fifo_miss_ratio = fifo_misses / total_pages

lru_hit_ratio = lru_hits / total_pages
lru_miss_ratio = lru_misses / total_pages


print("\n----- FIFO Page Replacement -----")
print("Hits:", fifo_hits)
print("Misses:", fifo_misses)
print("Hit Ratio:", round(fifo_hit_ratio, 2))
print("Miss Ratio:", round(fifo_miss_ratio, 2))

print("\n----- LRU Page Replacement -----")
print("Hits:", lru_hits)
print("Misses:", lru_misses)
print("Hit Ratio:", round(lru_hit_ratio, 2))
print("Miss Ratio:", round(lru_miss_ratio, 2))
