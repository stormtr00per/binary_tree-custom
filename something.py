from __future__ import print_function


training_data = [
    ['0' ,'0' ,'0' ,'0' ,'s1'],
    ['1' ,'0' ,'0' ,'0' ,'s2'],
    ['0' ,'1' ,'0' ,'0' ,'s3'],
    ['1' ,'1' ,'1' ,'0' ,'s4'],
    ['0' ,'1' ,'0' ,'1' ,'s5'],
    ['1' ,'0' ,'0' ,'0' ,'s6'],
    ['0' ,'1' ,'1' ,'1' ,'s7'],
    ['1' ,'1' ,'1' ,'1' ,'s8'],
    ['0' ,'0' ,'0' ,'0' ,'s9'],
    ['1' ,'1' ,'0' ,'0' ,'s10'],
    ['1' ,'1' ,'1' ,'1' ,'s11'],
    ['0' ,'1' ,'1' ,'0' ,'s12'],
    ['1' ,'0' ,'1' ,'1' ,'s13'],
    ['0' ,'0' ,'0' ,'1' ,'s14'],
    ['1' ,'0' ,'1' ,'0' ,'s15'],
    ['0' ,'1' ,'0' ,'1' ,'s16'],
    ['1' ,'0' ,'0' ,'0' ,'s17'],
    ['0' ,'0' ,'0' ,'0' ,'s18'],
    ['1' ,'1' ,'1' ,'1' ,'s19'],
    ['1' ,'1' ,'0' ,'0' ,'s20'],
    ['0' ,'0' ,'0' ,'0' ,'s21'],
    ['1' ,'1' ,'0' ,'1' ,'s22'],
    ['0' ,'1' ,'1' ,'0' ,'s23'],
    ['1' ,'1' ,'0' ,'0' ,'s24'],
    ['1' ,'0' ,'0' ,'0' ,'s25'],
    ['0' ,'0' ,'0' ,'1' ,'s26'],
    ['0' ,'1' ,'0' ,'0' ,'s27'],
    ['1' ,'1' ,'1' ,'1' ,'s28'],
    ['1' ,'0' ,'0' ,'1' ,'s29'],
    ['1' ,'0' ,'0' ,'1' ,'s30'],
    ['0' ,'1' ,'0' ,'1' ,'s31'],
    ['1' ,'0' ,'1' ,'0' ,'s32'],
    ['0' ,'0' ,'0' ,'1' ,'s33'],
    ['0' ,'0' ,'0' ,'0' ,'s34'],
]
header = ["AJ","Java","C++","C","students"]


def unique_vals(rows, col):
    return set([row[col] for row in rows])

def class_counts(rows):
    counts = {}
    for row in rows:mn
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)
class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def gini(rows):

    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):

    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)



def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1
    for col in range(n_features):
        values = set([row[col] for row in rows])
        for val in values:
            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print (spacing + str(node.question))
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs

if __name__ == '__main__':

    my_tree = build_tree(training_data)

    print_tree(my_tree)
    
    testing_data = [
        ['' ,'0' ,'0' ,'0' ,'t1'],
        ['' ,'1' ,'1' ,'0' ,'t2'],
        ['' ,'1' ,'0' ,'1' ,'t3'],
        ['' ,'0' ,'1' ,'1' ,'t4'],
        ['' ,'0' ,'0' ,'1' ,'t5'],
    ]

    for row in testing_data:
        print ("Actual: %s. Predicted: %s" %
               (row[-1], print_leaf(classify(row, my_tree))))
