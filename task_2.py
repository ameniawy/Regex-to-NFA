
from InfixToPostfix import Conversion
import argparse

# {
#     initial_state: s0,
#     final_states: [s1, s3],
#     states: [s1, s2, s3, s4, s5],
#     transitions: [
#         {
#             arc_from: s1,
#             arc_to: [s2, s4],
#             arc_condition: 'a'
#         }
#     ]
# }


class NFA:
    def __init__(self, initial_state, final_states, states, transitions):
        self.initial_state = initial_state
        self.final_states = final_states
        self.states = states
        self.transitions = transitions
        self.alphabets = []

    def add_transition(self, arc_from, arc_to, arc_condition):
        similar = [(index, transition) for (index, transition) in enumerate(self.transitions)
                   if transition['arc_from'] == arc_from and transition['arc_condition'] == arc_condition]

        # based on the implementation length will always be either 1 or 0
        if len(similar) == 0:
            transition = dict()
            transition['arc_from'] = arc_from
            transition['arc_to'] = [arc_to]
            transition['arc_condition'] = arc_condition
            self.transitions.append(transition)
            return

        # if transition from same state with same condition exists
        self.transitions[similar[0][0]]['arc_to'].append(arc_to)

    def get_alphabet(self):
        alpha = set()

        for trans in self.transitions:
            alpha.add(trans['arc_condition'])

        return list(alpha)

    def display(self):
        # print states
        res = ','.join([str(state) for state in self.states]) + '\n'
        # print alphabet
        res = res + ','.join(self.get_alphabet()) + '\n'
        # print start state
        res = res + str(self.initial_state) + '\n'
        # print final state(s)
        res = res + ','.join([str(state)
                              for state in self.final_states]) + '\n'
        # print transitions
        res = res + ', '.join(['(' + str(transition['arc_from']) + ',' + str(transition['arc_condition']) +
                               ',[' + ','.join([str(to) for to in transition['arc_to']]) + '])' for transition in self.transitions])
        return res


state_index = 0


def _create_state():
    global state_index
    new_state = state_index
    state_index += 1
    return new_state


def zero_or_more(nfa_1):
    """ Applies the kleene star operation on the input NFA and returns it.

    Parameters:
        nfa_1 (NFA): The NFA that we want to apply kleene star operation on.

    Returns:
        nfa_1 (NFA): The updated NFA after applying the kleene star operation on it.   

    """
    # 1 connect old final states with old initial state using epsilon transition
    for final_state in nfa_1.final_states:
        nfa_1.add_transition(final_state, nfa_1.initial_state, ' ')

    # 2 create a new initial state and connect it to the old initial state with an epsilon transition, old initial state is now a normal state
    new_initial_state = _create_state()
    nfa_1.states.append(new_initial_state)
    nfa_1.add_transition(new_initial_state, nfa_1.initial_state, ' ')
    nfa_1.initial_state = new_initial_state

    # 3 create a new acceptance state
    # 4 connect all old acceptance states to new acceptance state using epsilon transitions
    new_final_state = _create_state()
    nfa_1.states.append(new_final_state)
    for final_state in nfa_1.final_states:
        nfa_1.add_transition(final_state, new_final_state, ' ')

    nfa_1.final_states = [new_final_state]

    # 5 connect new start state to new acceptance state using epsilon transition
    nfa_1.add_transition(new_initial_state, new_final_state, ' ')

    # 6 return updated NFA after applying kleene star
    return nfa_1


def union(nfa_1, nfa_2):
    """ Creates a new NFA and applies union on input NFAs then return the new NFA.

    Parameters:
        nfa_1 (NFA): First NFA in the union operation.
        nfa_2 (NFA): Second NFA in the union operation.

    Returns:
        new_nfa (NFA): The new NFA after applying the union operation.

    """
    # 1 create a new NFA with states and transitions from both NFAs
    new_nfa = NFA(0, [], nfa_1.states + nfa_2.states,
                  nfa_1.transitions + nfa_2.transitions)

    # 2 create a new initial state and create epsilon transitions from it to
    # initial states of both NFAs and set it as initial state for new NFA
    new_initial_state = _create_state()

    new_nfa.add_transition(new_initial_state, nfa_1.initial_state, ' ')
    new_nfa.add_transition(new_initial_state, nfa_2.initial_state, ' ')

    new_nfa.initial_state = new_initial_state

    # 3 create a new final state and create epsilon transitions from old final states to new final state
    new_final_state = _create_state()
    for final_state in nfa_1.final_states:
        new_nfa.add_transition(final_state, new_final_state, ' ')

    for final_state in nfa_2.final_states:
        new_nfa.add_transition(final_state, new_final_state, ' ')

    new_nfa.final_states = [new_final_state]
    new_nfa.states += [new_initial_state, new_final_state]

    # 4 return new NFA
    return new_nfa


def concat(nfa_1, nfa_2):
    """ Creates a new NFA and applies concat on input NFAs then return the new NFA.

    Parameters:
        nfa_1 (NFA): First NFA in the union operation.
        nfa_2 (NFA): Second NFA in the union operation.

    Returns:
        new_nfa (NFA): The new NFA after applying the concat operation.

    """
    removed_state = nfa_1.final_states[0]
    nfa_1.states.remove(removed_state)

    for (idx1, transition) in enumerate(nfa_1.transitions):
        if transition['arc_from'] == removed_state:
            nfa_1.transitions[idx1]['arc_from'] = nfa_2.initial_state
        for (idx2, arc_to) in enumerate(transition['arc_to']):
            if arc_to == removed_state:
                nfa_1.transitions[idx1]['arc_to'][idx2] = nfa_2.initial_state

    # 1 create an epsilon transition between the final state(s) of nfa_1 to the initial_state of nfa_2
    new_nfa = NFA(nfa_1.initial_state, nfa_2.final_states, nfa_1.states +
                  nfa_2.states, nfa_1.transitions + nfa_2.transitions)

    # for final_state in nfa_1.final_states:
    #     new_nfa.add_transition(final_state, nfa_2.initial_state, ' ')

    # 2 final state of nfa_2 is the final state of the concat res
    # new_nfa.final_states = nfa_2.final_states

    return new_nfa


def copy_NFA(nfa_1):

    transitions = [{'arc_from': transition['arc_from'], 'arc_to': transition['arc_to'].copy(
    ), 'arc_condition': transition['arc_condition']} for transition in nfa_1.transitions]

    new_nfa = NFA(nfa_1.initial_state, nfa_1.final_states.copy(),
                  nfa_1.states.copy(), transitions)

    mapping = dict()

    for state in new_nfa.states:
        new_state = _create_state()
        mapping[state] = new_state

    for index, state in enumerate(new_nfa.states):
        new_nfa.states[index] = mapping[state]

    for index, state in enumerate(new_nfa.final_states):
        new_nfa.final_states[index] = mapping[state]

    new_nfa.initial_state = mapping[new_nfa.initial_state]

    for index, transition in enumerate(new_nfa.transitions):
        new_nfa.transitions[index]['arc_from'] = mapping[new_nfa.transitions[index]['arc_from']]

        for index_2, arc_to_instance in enumerate(transition['arc_to']):
            new_nfa.transitions[index]['arc_to'][index_2] = mapping[arc_to_instance]

    return new_nfa


def one_or_more(nfa_1):
    """ Returns the concat of nfa_1 and zero_or_more(nfa_!).

    Parameters:
        nfa_1 (NFA): NFA to apply the + on.

    Returns:
        res (NFA): The new NFA after applying the + operation.

    """
    copied_nfa_1 = copy_NFA(nfa_1)
    return concat(nfa_1, zero_or_more(copied_nfa_1))


def zero_or_one(nfa_1):
    """ Applies the zero or one operation on the input NFA and returns it.

    Parameters:
        nfa_1 (NFA): The NFA that we want to apply zero or one operation on.

    Returns:
        nfa_1 (NFA): The updated NFA after applying the zero or one operation on it.   

    """
    # 1 connect old final states with old initial state using epsilon transition
    # for final_state in nfa_1.final_states:
    #     nfa_1.add_transition(final_state, nfa_1.initial_state, ' ')

    # 2 create a new initial state and connect it to the old initial state with an epsilon transition, old initial state is now a normal state
    new_initial_state = _create_state()
    nfa_1.states.append(new_initial_state)
    nfa_1.add_transition(new_initial_state, nfa_1.initial_state, ' ')
    nfa_1.initial_state = new_initial_state

    # 3 create a new acceptance state
    # 4 connect all old acceptance states to new acceptance state using epsilon transitions
    new_final_state = _create_state()
    nfa_1.states.append(new_final_state)
    for final_state in nfa_1.final_states:
        nfa_1.add_transition(final_state, new_final_state, ' ')

    nfa_1.final_states = [new_final_state]

    # 5 connect new start state to new acceptance state using epsilon transition
    nfa_1.add_transition(new_initial_state, new_final_state, ' ')

    # 6 return updated NFA after applying kleene star
    return nfa_1


def create_NFA_from_symbol(symbol):
    initial_state = _create_state()
    final_state = _create_state()
    nfa = NFA(initial_state, [final_state], [initial_state, final_state], [])
    nfa.add_transition(initial_state, final_state, symbol)
    return nfa


def regex_postix_to_NFA(regex_postfix):
    operators = ['.', '*', '+', '?', '|']

    stack = list()

    for char in regex_postfix:
        if char in operators:
            if char == '.':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(concat(op1, op2))
            elif char == '|':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(union(op1, op2))
            elif char == '*':
                op1 = stack.pop()
                stack.append(zero_or_more(op1))
            elif char == '+':
                op1 = stack.pop()
                stack.append(one_or_more(op1))
            elif char == '?':
                op1 = stack.pop()
                op2 = create_NFA_from_symbol(' ')
                stack.append(union(op1, op2))

        else:
            nfa = create_NFA_from_symbol(char)
            stack.append(nfa)
            # stack

    return stack.pop()


def regex_infix_to_postfix(regex):
    conversion = Conversion()
    return conversion.infixToPostfix(regex_preprocess(regex))


def regex_preprocess(regex):
    res = ''
    for (index, char) in enumerate(regex):
        if char == 'ε':
            res += ' '
        elif index > 0 and (char.isalpha() or char.isdigit() or char == '(') and regex[index - 1] != '|' and regex[index - 1] != '(':
            res += '.'
            res += char
        else:
            res += char
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    with open(args.file, "r") as file:
        for regex in file:
            res_nfa = regex_postix_to_NFA(regex_infix_to_postfix(regex))
            print(res_nfa.display())

            output_file = open("task_2_result.txt", "w+")
            output_file.write(res_nfa.display())
