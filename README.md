# master-symbolic-and-distributed-artificial-intelligence

```prolog
%%%%%%%%%%%%%   ES1   %%%%%%%%%%%%%%
%%%%%%%         DOMINO        %%%%%%%%%
%%%%%%%%%%%%%  5 POINTS %%%%%%%%%%%%%%%
%
% Given the following clauses and facts

dfscc_solve(Node, Solution) :-
dfscc([], Node, Solution).

dfscc(Path, Node, FinalSolution) :- 
final(Node),
append(Path, [Node], FinalSolution).    

dfscc(Path, Node, Solution) :-
move(Node, Node1),
not(member(Node1, Path)), 
append(Path, [Node], PathNew),    
dfscc(PathNew, Node1, Solution).

final(config(hand([]), table(_))).

% Implement the move(Configuration1, Configuration2) predicate that succeeds if Configuration2 can be obtained starting from Configuration1 via a feasible Domino move, as explained in the textual part of the exam specification.

% Experiments

a1(Solution) :-
     dfscc_solve(config(
        hand([(2,5), (4,4), (4,0), (0,2), (4,3)]),  
        table([])), Solution).

/* 
 * false
*/

a2(Solution) :-
     dfscc_solve(config(
        hand([(2,5), (4,5), (0,2), (4,3), (6, 3), (6, 6)]),  
        table([])), Solution).

/* 
 * X = [config(hand([(2,5), (4,5), (0,2), (4,3), (6,3), (6,6)]),(table[])), 
 * config(hand([(4,5), (0,2), (4,3), (6,3), (6,6)]),(table[(2,5)])), 
 * config(hand([(4,5), (0,2), (4,3), (6,3)]),(table[(6,6), (2,5)])), 
 * config(hand([(4,5), (4,3), (6,3)]),(table[(0,2), (6,6), (2,5)])), 
 * config(hand([(4,5), (6,3)]),(table[(0,2), (6,6), (2,5), (3,4)])), 
 * config(hand([(6,3)]),(table[(0,2), (6,6), (2,5), (3,4), (4,5)])), 
 * config(hand([]),(table[(0,2), (6,6), (2,5), (3,4), (4,5), (3,6)]))]
 */

a3(Solution) :-
     dfscc_solve(config(
        hand([(2,5), (4,4), (4,5), (4,3)]),  
        table([(6, 4)])), Solution).

/*  
 * 
 * X = [config(hand([(2,5), (4,4), (4,5), (4,3)]),(table[(6,4)])), 
 * config(hand([(4,4), (4,5), (4,3)]),(table[(5,2), (6,4)])), 
 * config(hand([(4,4), (4,5)]),(table[(4,3), (5,2), (6,4)])), 
 * config(hand([(4,5)]),(table[(4,4), (4,3), (5,2), (6,4)])), 
 * config(hand([]),(table[(5,4), (4,4), (4,3), (5,2), (6,4)]))]*/


% CASE 1
% There are no tiles on the table: by using the predicate "select", one tile from the hand is 
% selected, removed from the hand and put on the table.
% Note that "select" selects the first element of the list first, but if called in backtracking 
% it selects the second, then the third, etc. 

move(
config(hand(ListHand), table([])), 
config(hand(NewListHand), table([Elem]))) :-
	select(Elem, ListHand, NewListHand).


% CASE 2
% The table is not empty and the last tile in the table has "LastE2" as free end; I discover which is 
% the last tile on the table by using length, and then picking the element in position L, where L
% is the lenght. This way, I pick the last element. The use of length and nth1 was suggested in the text. 
% I use "select" to look for a tile in my hand, that can connect with "LastE2", namely that summed to "LastE2" gives 8; 
% this tile, represented by (EinMyHand,NewLast), is removed from the hand (this is done automatically by select) 
% and I add it to the end of the table list, by using append.

move(
config(hand(ListHand), table([H|T])), 
config(hand(NewListHand), table(NewList))) :-
	length([H|T], L),
	nth1(L,[H|T],(_,LastE2)),
	select((EinMyHand,NewLast), ListHand, NewListHand),
	8 is EinMyHand+LastE2, % note here the condition to attach two tiles: adjiacent dots must give 8 as sum
	append([H|T],[(EinMyHand,NewLast)],NewList).

%%% IMPLEMENT THE OTHER CASES FOR MOVE %%%

% to be checked not sure 
move(
config(hand(ListHand), table([H|T])), 
config(hand(NewListHand), table(NewList))) :-
	length([H|T], L),
	nth1(L,[H|T],(_,LastE2)),
	select((NewLast, EinMyHand), ListHand, NewListHand),
	8 is EinMyHand+LastE2, % note here the condition to attach two tiles: adjiacent dots must give 8 as sum
	append([H|T],[(EinMyHand,NewLast)],NewList).


% Add to the left
move(
config(hand(ListHand), table([(F,X)|T])), 
config(hand(NewList), table([(Z,Y)|[(F,X)|T]]))) :-
	select((Z,Y), ListHand, NewList),
    8 is Y+F.

move(
config(hand(ListHand), table([(F,X)|T])), 
config(hand(NewList), table([(Z,Y)|[(F,X)|T]]))) :-
	select((Y,Z), ListHand, NewList),
    8 is Y+F.

%%%%%%%%%%%%%%%%   ES2   %%%%%%%%%%%%%%
%%%%%%% TAXONOMICAL REASONING %%%%%%%%%
%%%%%%%%%%%%%  5 POINTS %%%%%%%%%%%%%%%

% The Computer Science Ontology (CSO, https://cso.kmi.open.ac.uk/home) is a large-scale ontology of research areas that was automatically generated starting from about 16 million publications, mainly in the field of Computer Science. As its name suggests, it provides a taxonomy of Computer Science topics. 

% Consider the super_topic facts listed below, most of which are taken from the CSO Ontology, that relate a set of topics with their super-topic, which can in turn have a super-topic, and so on. 

super_topic([manifold_learning, dimensionality_reduction_method, 
dimensionality_reduction_techniques, dimensionality_reduction_algorithms, 
curse_of_dimensionality, subspace_learning, fisher_discriminant_analysis, 
small_sample_size_problems], 
            dimensionality_reduction).

super_topic([manifold_learning_algorithm, nonlinear_dimensionality_reduction, 
locally_linear_embedding, low-dimensional_manifolds, low-dimensional_spaces, isomap,
local_geometry, data_manifolds, nonlinear_manifolds, intrinsic_dimensions, neighborhood_graphs], 
            manifold_learning).

super_topic([dimensionality_reduction],
computer_science).

super_topic([image_subtraction, nonrigid_registration], 
subtraction_technique).

super_topic([subtraction_technique], 
automated_pattern_recognition).

super_topic([automated_pattern_recognition, neural_network, deep_neural_network, reinforcement_learning], 
machine_learning).

super_topic([machine_learning, knowledge_representation, planning, reasoning, multi_agent_systems], artificial_intelligence).

super_topic([artificial_intelligence],
computer_science).

% Implement a predicate all_supertopics(Topic, ListOfSuperTopics) that, given a topic as first argument, unifies ListOfSuperTopics with all the super topics.
% all_supertopic(Topic, ListOfSuperTopics) :-
    
    
% Implement a predicate all_subtopics(Topic, ListOfSubTopics) that, given a topic as first argument, unifies ListOfSubTopics with all the sub-topics.

% Note that some topics have no supertopic or subtopic.

% Experiments 

all_tests2(A, B, C, D, E, F, G) :-
   b1(A), b2(B), b3(C), b4(D), b5(E), b6(F), b7(G).


b1(Result) :- all_supertopics(subtraction_technique, Result).
%
b2(Result) :- all_supertopics(manifold_learning_algorithm, Result).
% 
b3(Result) :- all_subtopics(computer_science, Result).
% 
b4(Result) :- all_subtopics(manifold_learning, Result).
% 
b5(Result) :- all_subtopics(dimensionality_reduction, Result).
% 
b6(Result) :- all_subtopics(subspace_learning, Result).
%
b7(Result) :- all_supertopics(computer_science, Result).


/* Result to all_tests2(A, B, C, D, E, F, G)

A = [automated_pattern_recognition, machine_learning, artificial_intelligence, computer_science],

B = [manifold_learning, dimensionality_reduction, computer_science],

C = [dimensionality_reduction, artificial_intelligence, manifold_learning, dimensionality_reduction_method, dimensionality_reduction_techniques, dimensionality_reduction_algorithms, curse_of_dimensionality, subspace_learning, fisher_discriminant_analysis, small_sample_size_problems, manifold_learning_algorithm, nonlinear_dimensionality_reduction, locally_linear_embedding, low-dimensional_manifolds, low-dimensional_spaces, isomap, local_geometry, data_manifolds, nonlinear_manifolds, intrinsic_dimensions, neighborhood_graphs, image_subtraction, nonrigid_registration, subtraction_technique, automated_pattern_recognition, neural_network, deep_neural_network, reinforcement_learning, machine_learning, knowledge_representation, planning, reasoning, multi_agent_systems],

D = [manifold_learning_algorithm, nonlinear_dimensionality_reduction, locally_linear_embedding, low-dimensional_manifolds, low-dimensional_spaces, isomap, local_geometry, data_manifolds, nonlinear_manifolds, intrinsic_dimensions, neighborhood_graphs],

E = [manifold_learning, dimensionality_reduction_method, dimensionality_reduction_techniques, dimensionality_reduction_algorithms, curse_of_dimensionality, subspace_learning, fisher_discriminant_analysis, small_sample_size_problems, manifold_learning_algorithm, nonlinear_dimensionality_reduction, locally_linear_embedding, low-dimensional_manifolds, low-dimensional_spaces, isomap, local_geometry, data_manifolds, nonlinear_manifolds, intrinsic_dimensions, neighborhood_graphs],

F = G, G = []

*/

```
