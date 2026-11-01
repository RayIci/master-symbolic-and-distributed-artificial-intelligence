# Description

Jason on GitHub: [Jason](https://jason-lang.github.io); code on [Github Releses](https://github.com/jason-lang/jason/releases).

[Exercises #1](https://2026.aulaweb.unige.it/pluginfile.php/197298/mod_url/intro/excercises-on-beliefs-and-rules.pdf)
[Exercises #2](https://2026.aulaweb.unige.it/pluginfile.php/197298/mod_url/intro/excercises-on-negation-and-plans.pdf)
[Exercises #3](https://2026.aulaweb.unige.it/pluginfile.php/197298/mod_url/intro/excercises-on-communication.pdf?time=1763111746417)

Slides with BNF of the AgentSpeak Language

Some pieces of code developed on November 10, 2025; we still need to show plans triggered by the addition/removal of beliefs.

```Java
// Agent sample_agent in project mymas

stored(eggplant, 100).
stored(salad, 1200).
stored(tomato, 250).
stored(potato, 480).
stored(orange, 100).
stored(lemon, 200).
stored(lime, 50).
stored(grapefruit, 400).
stored(eggs, 2000).




transitive_stored(Superclass, Amount) :-

.findall(st(Subclass, X),
(stored(Subclass, X) & transitive_isa(Subclass, Superclass)),
ListWithAmount)

&
.print("Stored amount of ", Superclass, ": ", ListWithAmount, "\n")
&
sum(ListWithAmount, Amount).

isa(orange, citrus).
isa(lemon, citrus).
isa(lime, citrus).
isa(grapefruit, citrus).
isa(citrus, fruit).
isa(fruit, vegetable).
isa(eggplant, vegetable).
isa(potato, vegetable).
isa(tomato, vegetable).
isa(salad, vegetable).

transitive_isa(X, Y) :- isa(X, Y).
transitive_isa(X, Z) :- isa(X, Y) & transitive_isa(Y, Z).

sum([], 0).
sum([st(_, A)|T], Res+A) :- sum(T, Res).


/* Initial goals */
!start.

/* Plans */
+!start : transitive_stored(citrus, Y) <-
!printAmount(Y);
-stored(lime, _);
+stored(mandarino, 600);
+isa(mandarino, citrus);
?transitive_stored(citrus, Z);
!printAmount(Z).

+!printAmount(Y) : true <-
.print("How many citrus are stored today FAIL: ", Y); Y < 100.

-!printAmount(Y) : true <- .print("How many citrus are stored today RECOVERY: ", Y).
```
