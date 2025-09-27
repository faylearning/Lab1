# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
import numpy as np

class TextbookStack(object):
    """ A class that tracks the """
    def __init__(self, initial_order, initial_orientations):
        assert len(initial_order) == len(initial_orientations)
        self.num_books = len(initial_order)
        
        for i, a in enumerate(initial_orientations):
            assert i in initial_order
            assert a == 1 or a == 0

        self.order = np.array(initial_order)
        self.orientations = np.array(initial_orientations)

    def flip_stack(self, position):
        assert position <= self.num_books
        
        self.order[:position] = self.order[:position][::-1]
        self.orientations[:position] = np.abs(self.orientations[:position] - 1)[::-1]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)
    
    def __eq__(self, other):
        assert isinstance(other, TextbookStack), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(self.orientations == other.orientations)

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack


def createHash(stack_obj):
        order_str = ','.join(map(str, stack_obj.order))
        orient_str = ','.join(map(str, stack_obj.orientations))
        return f"{order_str}|{orient_str}"



def breadth_first_search(stack):
    flipList = []

    # --- v ADD YOUR CODE HERE v --- #
    if stack.check_ordered():
        return flipList
    
    exqueue = deque()
    exqueue.append((stack, []))
    visited = set()
    visited.add(createHash(stack))
    
    while exqueue:
        currbooks, path_so_far = exqueue.popleft()
        
        #every possible flip operation
        for flip_at in range(1, currbooks.num_books + 1):
            new_books = currbooks.copy()
            new_books.flip_stack(flip_at)
            new_path = path_so_far + [flip_at]
        
            if new_books.check_ordered():
                return new_path
            
            #avoid revisiting 
            state_hash = createHash(new_books)
            if state_hash not in visited:
                visited.add(state_hash)
                exqueue.append((new_books, new_path))
    
    return flipList
    # ---------------------------- #


def depth_first_search(stack):
    flipList = []

    # --- v ADD YOUR CODE HERE v --- #
    if stack.check_ordered():
        return flipList
    
    work_stack = [(stack, [])]
    explored = set()
    
    explored.add(createHash(stack))
    
    while work_stack:
        book_config, moves_made = work_stack.pop()
        
        #all possible next moves
        for move in range(1, book_config.num_books + 1):
            next_config = book_config.copy()
            next_config.flip_stack(move)
            updated_moves = moves_made + [move]
            
            #check if solved
            if next_config.check_ordered():
                return updated_moves
            
            #skip if visited
            config_id = createHash(next_config)
            if config_id not in explored:
                explored.add(config_id)
                work_stack.append((next_config, updated_moves))
    
    return flipList
    # ---------------------------- #