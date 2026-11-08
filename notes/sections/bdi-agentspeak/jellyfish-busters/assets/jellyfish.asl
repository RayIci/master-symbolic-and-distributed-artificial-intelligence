/* Initial beliefs */
adjacent(a, b).
adjacent(b, c).
adjacent(c, d).
location(myself, a).
location(jellyfish, b).
location(bin, d).

/* Initial goal */
!bust_jellyfishes.

/* Plan 1 */
+!bust_jellyfishes :
    location(myself, X) &
    location(jellyfish, X) &
    location(bin, Y)
 <- !pick(jellyfish, X);
    move_to(Y);
    !drop(jellyfish, Y).

/* Plan 2 */
+!bust_jellyfishes :
    location(myself, X) &
    not location(jellyfish, X) &
    adjacent(X, Z)
 <- move_to(Z);
    !bust_jellyfishes.
