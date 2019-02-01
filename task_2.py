

# initial state
# final states
# states
# transitions
# {
#     initial_state: s0,
#     final_states: [s1, s3],
#     states: [s1, s2, s3, s4, s5],
#     transitions: [
#         {
#             arc_from: s1,
#             arc_to: s2,
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

    def set_initial_state(self, initial_state):
        raise NotImplementedError

state_index = 0

def _create_transition(arc_from, arc_to, arc_condition):
    transition = dict()
    transition['arc_from'] = arc_from
    transition['arc_to'] = arc_to
    transition['arc_condition'] = arc_condition
    return transition  

def _create_state():
    global state_index
    new_state = state_index
    state_index += 1
    return new_state


def kleene(nfa_1):
    """ Applies the kleene star operation on the input NFA and returns it.

    Parameters:
        nfa_1 (NFA): The NFA that we want to apply kleene star operation on.

    Returns:
        nfa_1 (NFA): The updated NFA after applying the kleene star operation on it.   

    """
    # 1 connect old final states with old initial state using epsilon transition
    for final_state in nfa_1.final_states:
        transition = _create_transition(final_state, nfa_1.initial_state, 'eps')
        nfa_1.transitions.append(transition)

    # 2 create a new initial state and connect it to the old initial state with an epsilon transition, old initial state is now a normal state
    new_initial_state = _create_state()
    nfa_1.states.append(new_initial_state)
    transition = _create_transition(new_initial_state, nfa_1.initial_state, 'eps')
    nfa_1.transitions.append(transition)
    nfa_1.initial_state = new_initial_state

    # 3 create a new acceptance state
    # 4 connect all old acceptance states to new acceptance state using epsilon transitions
    new_final_state = _create_state()
    nfa_1.states.append(new_final_state)
    for final_state in nfa_1.final_states:
        transition = _create_transition(final_state, new_final_state, 'eps')
        nfa_1.transitions.append(transition)
    
    nfa_1.final_states = [new_final_state]

    # 5 connect new start state to new acceptance state using epsilon transition
    transition = _create_transition(new_initial_state, new_final_state, 'eps')
    nfa_1.transitions.append(transition)

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
    new_nfa = NFA(0,[], nfa_1.states + nfa_2.states, nfa_1.transitions + nfa_2.transitions)

    # 2 create a new initial state and create epsilon transitions from it to
    # initial states of both NFAs and set it as initial state for new NFA
    new_initial_state = _create_state()

    transition_1 = _create_transition(new_initial_state, nfa_1.initial_state, 'eps')
    transition_2 = _create_transition(new_initial_state, nfa_2.initial_state, 'eps')
    new_nfa.transitions.append(transition_1)
    new_nfa.transitions.append(transition_2)
    new_nfa.initial_state = new_initial_state

    # 3 create a new final state and create epsilon transitions from old final states to new final state
    new_final_state = _create_state()
    for final_state in nfa_1.final_states:
        transition_1 = _create_transition(final_state, new_final_state, 'eps')
        new_nfa.transitions.append(transition_1)

    for final_state in nfa_2.final_states:
        transition_1 = _create_transition(final_state, new_final_state, 'eps')
        new_nfa.transitions.append(transition_1)

    # 4 return new NFA
    return new_nfa




