mergeSort([], []).
mergeSort([A], [A]).
mergeSort([A, B | Rest], S) :- divide([A, B | Rest], L1, L2),
mergeSort(L1, S1),
mergeSort(L2, S2),
merge(S1, S2, S).
divide([], [], []).
divide([A], [A], []).
divide([A, B | R], [A | Ra], [B | Rb]) :- divide(R, Ra, Rb).
merge(A, [], A).
merge([], B, B).
merge([A | Ra], [B | Rb], [A | M]) :- A =< B, merge(Ra, [B | Rb], M).
merge([A | Ra], [B | Rb], [B | M]) :- A > B, merge([A | Ra], Rb, M).
?- mergeSort([3, 4, 8, 0, 1, 9, 5, 6], Sorted).
