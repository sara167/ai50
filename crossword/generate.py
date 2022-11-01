import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # loop over each variable
        for v in self.domains:
            # for each variable, loop over its domains
            domains = self.domains[v]
            domains_copy = set([i for i in domains])

            for word in domains_copy:
                # if it doesn't satisfy the unary constraint, remove it
                if len(word) != v.length:
                    domains.remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        what are the constraint?
        - no mutual words
        - if overlap, ith character of v1’s value must be the same as the jth character of v2’s value
        """
        revised = False

        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False

        domains_copy = set([i for i in self.domains[x]])

        for X in self.domains[x]:
            for Y in self.domains[y]:
                # if overlapping correctly, don't remove from x
                if X[overlap[0]] == Y[overlap[1]]:
                    break
                # if found in both
                if X == Y and X in domains_copy:
                    domains_copy.remove(X)
                    revised = True

        self.domains[x] = domains_copy
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = []
            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if v1 != v2:
                        arcs.append((v1, v2))


        while len(arcs) > 0:
            (x, y) = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z!= y:
                        arcs.append((z, x))
            else:
                break

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment:
                return False
            if assignment[v] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        used_words = []
        for (v, word) in assignment.items():
            # check duplicates
            if word in used_words:
                return False
            else:
                used_words.append(word)

            # check word's length
            if v.length != len(word):
                return False

            # check conflicting neighbors
            neighbors = self.crossword.neighbors(v)
            for n in neighbors:
                overlap = self.crossword.overlaps[v,n]
                if overlap is not None and n in assignment:
                    if word[overlap[0]] != str(assignment[n])[overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # initialize counting list
        values = []

        # find neighbors
        neighbors = self.crossword.neighbors(var)

        # loop over the domain values of var
        for v in self.domains[var]:

            if v in assignment:
                continue

            else:

                # initialize count variable to count eliminated values
                count = 0

                # loop over the neighbors
                for n in neighbors:

                    # if var and n has the same word --> eliminate
                    if v in self.domains[n]:
                        count += 1

                values.append([v, count])

        values.sort(key=lambda x: x[1])
        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = []
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned.append(var)

        minRemainingValues = [unassigned[0]]

        # Choose the variable with the minimum number of remaining values in its domain
        for var in unassigned:
            if len(self.domains[minRemainingValues[0]]) > len(self.domains[var]):
                minRemainingValues.pop()
                minRemainingValues.append(var)
            elif len(self.domains[minRemainingValues[0]]) == len(self.domains[var]):
                minRemainingValues.append(var)

        # If there is a tie, choose the variable with the highest degree.
        if len(minRemainingValues) == 1:
            return minRemainingValues[0]
        else:
            highestdegree = [minRemainingValues[0]]
            for var in minRemainingValues:
                hd = highestdegree.pop()
                hvar = self.order_domain_values(var, assignment)
                hfar = self.order_domain_values(hd, assignment)
                if len(hvar) ==0:
                    highestdegree.append(hd)
                    continue
                else:
                    highest_in_var = hvar.pop()[1]
                    highest_so_far = hfar.pop()[1]
                    if highest_so_far < highest_in_var:
                        highestdegree.append(var)
                    elif highest_in_var == highest_so_far:
                        highestdegree.append(hd)
                        highestdegree.append(var)
            # If there is a tie, any of the tied variables are acceptable return values
            return highestdegree[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment)[::-1]:
            assignment[var] = value[0]
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
