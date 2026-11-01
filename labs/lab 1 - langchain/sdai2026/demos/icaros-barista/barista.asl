// Demo for the SDAI 2026 lab slides, adapted from icaros examples/missing-plan:
// .println instead of .print, and the MAS stops itself at the end (.stopMAS)
// so that the ▶ button in the slides sees the run finish.
//
// An agent that knows how to do the four steps of making a coffee, and does
// NOT know how to make a coffee. The plan that would tie them together is the
// one thing missing from this file -- see the bottom.
//
// Each step is guarded by what it needs and asserts what it produced, so the
// order is not decoration: call !brew before there are grounds and no plan is
// applicable, the goal fails, and the failure is what the caller finds out.
//
// Only "/**" and "///" comments are read as documentation. The summary becomes
// the tool's description and @when tells the model when that version applies,
// so what is written here is quite literally what the model gets to read.

/**
 * Takes a bag of beans out of the cupboard.
 * @when there are no beans on the counter yet
 */
@p_fetch
+!fetch_beans
    <-  .println("fetching the beans");
        +have(beans).

/**
 * Grinds the beans that are on the counter.
 * @when there are beans and they have not been ground yet
 */
@p_grind
+!grind : have(beans)
    <-  .println("grinding");
        +have(grounds).

/**
 * Boils the water. Needs nothing: it can be done at any point.
 */
@p_boil
+!boil_water
    <-  .println("boiling the water");
        +have(hot_water).

/**
 * Brews the coffee from the grounds and the hot water.
 * @when there are already grounds AND the water is already hot
 */
@p_brew
+!brew : have(grounds) & have(hot_water)
    <-  .println("brewing");
        +have(coffee).

// THE MISSING PLAN. Written out here, and only here, as a comment:
//
//   +!make_coffee <- !fetch_beans; !grind; !boil_water; !brew.
//
// Nothing in the agent can do that. What happens instead is that .run opens a
// session and, for as long as it lasts, the model IS this plan: it asks for
// one goal at a time, is told what each one changed, and decides what to ask
// for next. Note that the composition lives in the session and dies with it --
// nothing is added to the plan library, and the next run starts over. icaros
// does not write the missing plan; at the "run" rung it lets a model stand in
// for one.
//
// Also note that !boil_water depends on nothing, so there is no single right
// sequence: the model has to respect a dependency, not reproduce a list.

+!start
    <-  .println("--- I have the steps but not the recipe ---");
        .run("Make a coffee. You have one goal per step; call them one at a time
              and read what each answer says it changed -- that is what tells you
              which step is possible next. What I currently believe is already in
              front of you, so do not spend turns looking it up. Call icaros_done
              as soon as I believe I have coffee.");
        .println("--- and now let me tell you what I did ---");
        .talk("You just made a coffee by asking me for one step at a time. Explain
               the coffee: which steps you asked for, in which order, and why that
               order was the one it had to be. Do not describe this conversation.", Answer);
        .println( Answer );
        .stopMAS.

// what a session that runs out of rounds looks like from the plan's side: the
// goal fails like any other, and this is the plan that catches it
-!start
    <-  .println("--- the model ran out of turns before there was coffee ---");
        .stopMAS.

!start.