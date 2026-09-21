# ==========================================================
# DISK SCHEDULING AND SIMPLE FILE SYSTEM DESIGN
# ==========================================================

import random


# ==========================================================
# PART 1: DISK SCHEDULING
# ==========================================================

def fcfs(requests, head):
    movement = 0
    current = head

    for request in requests:
        movement += abs(request - current)
        current = request

    return movement


def sstf(requests, head):
    requests = requests.copy()
    movement = 0
    current = head

    while requests:
        closest = min(requests, key=lambda x: abs(x - current))

        movement += abs(closest - current)
        current = closest
        requests.remove(closest)

    return movement


def c_scan(requests, head, disk_size):
    requests = sorted(requests)
    movement = 0
    current = head

    right = [x for x in requests if x >= head]
    left = [x for x in requests if x < head]

    for request in right:
        movement += abs(request - current)
        current = request

    if left:
        movement += (disk_size - 1) - current
        current = disk_size - 1

        movement += disk_size - 1
        current = 0

        for request in left:
            movement += abs(request - current)
            current = request

    return movement


def c_look(requests, head):
    requests = sorted(requests)
    movement = 0
    current = head

    right = [x for x in requests if x >= head]
    left = [x for x in requests if x < head]

    for request in right:
        movement += abs(request - current)
        current = request

    if left:
        movement += abs(current - left[0])
        current = left[0]

        for request in left[1:]:
            movement += abs(request - current)
            current = request

    return movement


def rss(requests, head):
    requests = requests.copy()
    random.seed(10)
    random.shuffle(requests)

    movement = 0
    current = head

    for request in requests:
        movement += abs(request - current)
        current = request

    return movement


# ==========================================================
# PART 2: SIMPLE FILE SYSTEM
# ==========================================================

class SimpleFileSystem:

    def __init__(self, total_blocks=20):
        self.total_blocks = total_blocks
        self.blocks = [None] * total_blocks
        self.directory = {}

    def create_file(self, filename, data):
        if filename in self.directory:
            print("File already exists.")
            return

        required_blocks = (len(data) + 9) // 10

        free_blocks = [
            i for i in range(self.total_blocks)
            if self.blocks[i] is None
        ]

        if len(free_blocks) < required_blocks:
            print("Not enough free blocks.")
            return

        allocated_blocks = free_blocks[:required_blocks]

        for block in allocated_blocks:
            self.blocks[block] = filename

        self.directory[filename] = {
            "data": data,
            "blocks": allocated_blocks
        }

        print("File created:", filename)
        print("Allocated blocks:", allocated_blocks)

    def read_file(self, filename):
        if filename not in self.directory:
            print("File not found.")
            return

        file = self.directory[filename]

        print("File:", filename)
        print("Data:", file["data"])
        print("Blocks:", file["blocks"])

    def delete_file(self, filename):
        if filename not in self.directory:
            print("File not found.")
            return

        blocks = self.directory[filename]["blocks"]

        for block in blocks:
            self.blocks[block] = None

        del self.directory[filename]

        print("File deleted:", filename)

    def show_directory(self):
        print("\nDirectory:")

        if not self.directory:
            print("Directory is empty.")
            return

        for filename, details in self.directory.items():
            print(
                filename,
                "-> Blocks:",
                details["blocks"]
            )

    def show_blocks(self):
        print("\nBlock Status:")

        for i in range(self.total_blocks):
            if self.blocks[i] is None:
                print("Block", i, ": Free")
            else:
                print("Block", i, ":", self.blocks[i])


# ==========================================================
# MAIN PROGRAM
# ==========================================================

# Predefined disk scheduling data
requests = [98, 183, 37, 122, 14, 124, 65, 67]
head = 53
disk_size = 200

print("=" * 50)
print("        DISK SCHEDULING SIMULATION")
print("=" * 50)

print("Requests:", requests)
print("Initial Head:", head)
print("Disk Size:", disk_size)

print("\nTotal Head Movement:")
print("FCFS   :", fcfs(requests, head))
print("SSTF   :", sstf(requests, head))
print("C-SCAN :", c_scan(requests, head, disk_size))
print("C-LOOK :", c_look(requests, head))
print("RSS    :", rss(requests, head))


# ==========================================================
# SIMPLE FILE SYSTEM DEMONSTRATION
# ==========================================================

print("\n" + "=" * 50)
print("        SIMPLE FILE SYSTEM")
print("=" * 50)

fs = SimpleFileSystem(20)

# Create files
fs.create_file("file1.txt", "Hello World")
fs.create_file("file2.txt", "Operating System Practical")

# Display directory
fs.show_directory()

# Read a file
print("\nReading file:")
fs.read_file("file1.txt")

# Delete a file
print("\nDeleting file:")
fs.delete_file("file1.txt")

# Display directory after deletion
fs.show_directory()

# Display block status
fs.show_blocks()
