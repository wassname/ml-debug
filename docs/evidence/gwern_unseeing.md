# Unseeing — Gwern Branwen

Source: https://gwern.net/unseeing (page title: "On Seeing Through and Unseeing: The Hacker Mindset")
Fetched-via: r.jina.ai reader, 2026-08-15 (CLAUDE agent)
Fetch-status: full article text, with the site's backlinks / similar-links / bibliography nav sections trimmed. Supersedes the earlier two-quote excerpt. (CLAUDE agent)

Why it matters here: why you cannot see your own work or data clearly, and why a single small anomaly can mean the everyday mental model is fundamentally wrong.

---

Defining the security/hacker mindset as extreme reductionism: ignoring the surface abstractions and limitations to treat a system as a source of parts to manipulate into a different system, with different (and usually unintended) capabilities.

> To draw some parallels here and expand [⁠Dullien 2017⁠](https://gwern.net/turing-complete#dullien-2017), I think [unexpected Turing-complete systems and weird machines⁠](https://gwern.net/turing-complete) have something in common with heist movies or cons or stage magic: they all share a specific paradigm we might call the _security mindset_ or _hacker mindset_.
> 
> 
> What they (and hacking, [speedrunning⁠](https://en.wikipedia.org/wiki/Speedrunning), [social-engineering⁠](https://en.wikipedia.org/wiki/Social_engineering_(security)) etc.) all have in common is that they show that the much-ballyhooed ‘hacker mindset’ is, fundamentally, a sort of reductionism run amok, where one [⁠‘sees through’⁠](https://gwern.net/doc/philosophy/epistemology/2012-sistery-tryingtoseethrough.html) abstractions to a manipulable reality. Like Neo in the _Matrix_—a deeply cliche analogy for hacking, but cliche because it resonates—one achieves enlightenment by seeing through the surface illusions of objects and can now see the endless lines of green code which make up the Matrix, and vice-versa. (It’s maps all the way down!)
> 
> 
> In each case, the fundamental principle is that the hacker asks: “here I have a system _W_, which pretends to be made out of a few [_X_ s⁠](https://github.com/kdeldycke/awesome-falsehood); however, it is **really** made out of many _Y_, which form an entirely different system, _Z_; I will now proceed to ignore the illusory _X_ and understand how _Z_ works, so I may use the _Y_ to thereby change _W_ however I like”.

[A](https://gwern.net/dropcap#kanzlei)bstractions are vital, but like many living things, dangerous, because [⁠abstractions always leak](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/). (“You’re very clever, young man, but it’s reductionism all the way down!”) This is in some sense the opposite of a mathematician: a mathematician tries to ‘see through’ a complex system’s accidental complexity up to a simpler more-abstract more-true version which can be understood & manipulated—but for the hacker, all complexity is essential, and they are instead trying to _un_ see the simple abstract system down to the more-complex less-abstract (but also more true) version.⁠[⁠1⁠](https://gwern.net/unseeing#fn1) (A mathematician might try to transform a program up into successively more abstract representations to eventually show it is trivially correct; a hacker would prefer to compile a program down into its most concrete representation to [brute force all execution paths⁠](https://gwern.net/forking-path)& find an exploit trivially proving it incorrect.)

## [Confirmation Bias](https://gwern.net/unseeing#confirmation-bias "Link to section: § 'Confirmation Bias'")

> [Uncle Milton Industries⁠](https://en.wikipedia.org/wiki/Milton_Levine) has been selling [ant farms⁠](https://en.wikipedia.org/wiki/Formicarium) to children since 1956 70ya. Some years ago, I remember opening one up with a friend. There were no actual ants included in the box. Instead, there was a card that you filled in with your address, and the company would mail you some ants.
> 
> 
> My friend expressed surprise that you could get ants sent to you in the mail. I replied: ‘What’s really interesting is that these people will send a tube of live ants to anyone you tell them to.’
> 
> 
> [Bruce Schneier⁠](https://en.wikipedia.org/wiki/Bruce_Schneier), [⁠“The Security Mindset”⁠](https://www.schneier.com/blog/archives/2008/03/the_security_mi_1.html) (2008 18ya); cf.[DNS](https://www.tbray.org/ongoing/When/202x/2022/06/02/Dangerous-Gift), [Mormons/JVs⁠](https://x.com/_JeanLannes/status/1687649736356982784)

![Image 1: The 1888 <a href='https://en.wikipedia.org/wiki/Flammarion_engraving'>Flammarion engraving</a> by <a href='https://en.wikipedia.org/wiki/Camille_Flammarion'>Camille Flammarion</a> (<a href='https://commons.wikimedia.org/wiki/File:Flammarion.jpg'>WMF</a>), illustrating, using a pastiche of a Renaissance woodblock engraving, a medieval missionary peeking out from Earth under the celestial sphere and seeing the mechanics of the universe for the first time.](https://gwern.net/doc/philosophy/epistemology/1888-flammarion-latmospheremetereorologiepopulaire-theflammarianengraving.jpg)
Ordinary users ask only that all their everyday examples of _Y_ s transforms into _Z_ correctly; they forget to ask whether all and _only_ correct examples of _Y_ s transform into correct _Z_ s, and whether only correct _Z_ s can be constructed to become _Y_ s. Even a single ‘anomaly’, apparently trivial in itself, can indicate the everyday mental model is not just a little bit wrong, but _fundamentally_ wrong, in the way that Newton’s theory of gravity is not merely a little bit wrong and just needs a quick patch with a fudge factor to account for [Mercury⁠](https://en.wikipedia.org/wiki/Two-body_problem_in_general_relativity#Anomalous_precession_of_Mercury) or that NASA management’s mental model of O-rings was [not merely⁠](https://en.wikipedia.org/wiki/Space_Shuttle_Challenger_disaster) in need of a minor increase in the thickness of the rubber gaskets⁠[⁠2⁠](https://gwern.net/unseeing#fn2).

## [Atoms](https://gwern.net/unseeing#atoms "Link to section: § 'Atoms'")

> Every drop of blood has great talent; the original cellule seems identical in all animals, and only varied in its growth by the varying circumstance which opens now this kind of cell and now that, causing in the remote effect now horns, now wings, now scales, now hair; and the same numerical atom, it would seem, was equally ready to be a particle of the eye or brain of man, or of the claw of a tiger…The man truly conversant with life knows, against all appearances, that there is a remedy for every wrong, and that every wall is a gate.
> 
> 
> [Ralph Waldo Emerson⁠](https://en.wikipedia.org/wiki/Ralph_Waldo_Emerson), “Natural History Of Intellect”, 1893⁠[⁠3⁠](https://gwern.net/unseeing#fn3)

It’s all “atoms and the void”⁠[⁠4⁠](https://gwern.net/unseeing#fn4):

*   In **hacking**, a computer pretends to be made out of things like ‘buffers’ and ‘lists’ and ‘objects’ with rich meaningful semantics, but really, it’s just made out of bits which mean nothing and only accidentally can be interpreted as things like ‘web browsers’ or ‘passwords’, and if you move some bits around and rewrite these other bits in a particular order and read one string of bits in a different way, now you have bypassed the password.

*   In [**speed running**⁠](https://en.wikipedia.org/wiki/Speed_running) (particularly [TASes⁠](https://en.wikipedia.org/wiki/Tool-assisted_speedrun)), a video game pretends to be made out of things like ‘walls’ and ‘speed limits’ and ‘levels which must be completed in a particular order’, but it’s really again just made out of bits and memory locations, and messing with them in particular ways, such as deliberately overloading the RAM [⁠to cause](https://threadreaderapp.com/thread/1148361355130527748.html)[⁠memory allocation](https://www.halopedia.org/Overload_Glitch_(Halo_3)) errors, can give you infinite ‘velocity’ or shift you into [⁠alternate coordinate systems in the true physics⁠](https://www.youtube.com/watch?v=wjge1bVobN0), allowing enormous movements in the supposed map, giving shortcuts to the ‘end’⁠[⁠5⁠](https://gwern.net/unseeing#fn5) of the game.

*   in [**stealth games**⁠](https://en.wikipedia.org/wiki/Stealth_games), players learn to unsee levels into patterns of gaps moving around over time—gaps in guard patrols or observability of light/sound—and how to dismantle the level piece by piece until they can go anywhere and do anything

*   In **breaking and entering**, like robbing a hotel room, people see ‘doors’ and ‘locks’ and ‘walls’, but really, they are just made out of atoms arranged in a particular order, and you can move some atoms around more easily than others, and instead of going through a ‘door’ you can just cut a hole in the [wall⁠](https://en.wikipedia.org/wiki/Drywall)⁠[⁠6⁠](https://gwern.net/unseeing#fn6) (or ceiling) and obtain access to a space. At Los Alamos, Richard Feynman, among other tactics, [obtained classified papers by reaching in underneath drawers⁠](https://gwern.net/doc/cs/cryptography/1985-feynman-surelyyourejokingmrfeynman-ch18-safecrackermeetsafecracker.pdf)& ignoring the locks entirely.

    *   One analysis of the movie _[Die Hard⁠](https://en.wikipedia.org/wiki/Die\_Hard)_, [⁠“Nakatomi space”⁠](https://bldgblog.com/2010/01/nakatomi-space/), highlights how it and the Israel military’s [_mouse-holing_⁠](https://en.wikipedia.org/wiki/Mouse-holing) in the [Battle of Nablus⁠](https://en.wikipedia.org/wiki/Battle_of_Nablus) treat buildings as kinds of machines, which can be manipulated in weird ways to move around to attack their enemies.

    *   That example reminds me of the [⁠Carr & Adey](https://bodiesfromthelibrary.com/2017/10/23/seven-types-of-locked-room-mystery-part-15/) anatomy of [_locked room murder mysteries_⁠](https://en.wikipedia.org/wiki/Locked-room_mystery), laying out a taxonomy of all the possible solutions which—like a magician’s trick—violate one’s assumptions about the locked room.

For example, whether the room was always locked, locked at the right time, the murder done while in the room, the murder done _before_ everyone entered the room, it being murder rather than suicide, the supposed secure room with locked-doors having a _ceiling_ etc.⁠[⁠7⁠](https://gwern.net/unseeing#fn7) (These tricks inspired [_Umineko_’s⁠](https://en.wikipedia.org/wiki/Umineko_When_They_Cry) mysteries ([review⁠](https://gwern.net/review/umineko)), although in it a lot of them turn out to just involve [⁠conspirators/lying⁠](https://07th-expansion.fandom.com/wiki/Willard's_Truths).)

    *   In [_⁠lockpicking_⁠](https://en.wikipedia.org/wiki/Lockpicking), copying a key or reverse-engineering its cuts are some of the most difficult ways to pick a lock. One can instead simply use a [bump key⁠](https://en.wikipedia.org/wiki/Lock_bumping) to brute-force the positions of the pins in a lock, or kick the door in, or [⁠among other door lock bypasses⁠](https://www.youtube.com/watch?v=4YYvBLAF4T8?t=330), wiggle the bolt, or reach through a crack to open from the inside, or drill the lock. (How do you know someone hasn’t already? You _assume_ it’s the same lock as yesterday?) If all else fails, you can use a portable [hydraulic ram⁠](https://en.wikipedia.org/wiki/Hydraulic_ram) as a spreader to shatter the frame or wall itself _around_ the door.

Locks & safes have many other interesting vulnerabilities; I particularly like [Matt Blaze’s⁠](https://en.wikipedia.org/wiki/Matt_Blaze)[master-key⁠](https://en.wikipedia.org/wiki/Master_keying) vulnerability ([⁠Blaze 2003⁠](https://www.mattblaze.org/papers/mk.pdf)/[⁠Blaze 2004 22ya a⁠](https://www.mattblaze.org/papers/safelocks.pdf)/[Blaze 2004 22ya b⁠](https://www.mattblaze.org/papers/humancambridgepreproc.pdf)), which uses the fact that a master-key lock is actually opening for any _combination_ of master+ordinary key cuts (ie. ‘master OR ordinary’ rather than ‘master XOR ordinary’), and so it is like a password which one can guess one letter at a time. (These papers made locksmiths so mad [they harassed Blaze into quitting⁠](https://x.com/mattblaze/status/1553254965870841856).)

*   In [**stage magic**⁠](https://en.wikipedia.org/wiki/Magic_(illusion)) (especially close-up/card/coin/pickpocketing), one believes one is continuously seeing single whole objects which must move from one place to another continuously; in reality, one is only seeing, occasionally, surfaces of many (possibly duplicate) objects, which may be moving only when you are not looking, in the opposite direction, or not moving at all. By hacking [object permanence⁠](https://en.wikipedia.org/wiki/Object_permanence) and limited [attentional⁠](https://en.wikipedia.org/wiki/Misdirection_(magic))[resources⁠](https://en.wikipedia.org/wiki/Change_blindness), the stage magician shows the ‘impossible’ ([Macknik et al 2008’s Table 1⁠](https://gwern.net/doc/psychology/cognitive-bias/illusion-of-depth/2008-macknik.pdf) lists many [folk physics⁠](https://en.wikipedia.org/wiki/Na%C3%AFve_physics) assumptions which can be hacked). Stage magic works by exploiting our implicit beliefs that no adversary would take the trouble to so precisely exploit our heuristics and shortcuts.⁠[⁠8⁠](https://gwern.net/unseeing#fn8)⁠[⁠9⁠](https://gwern.net/unseeing#fn9)

*   In **weird machines**, you have a ‘protocol’ like SSL or x86 machine code which appear to do simple things like ‘check a cryptographic signature’ or ‘add one number in a register to another register’, but in reality, it’s a layer over far more complex realities like processor states & optimizations like speculative execution reading other parts of memory and then quickly erasing it, and these can be pasted together to execute operations and reveal secrets without ever running ‘code’ (see again Mcilroy et al 2019).

Similarly, in finding hidden examples of Turing completeness, one says, ‘this system appears to be a bunch of dominoes or whatever, but actually, each one is a computational element which has unusual inputs/outputs; I will now proceed to wire a large number of them together to form a Turing machine so I can play Tetris in Conway’s Game of Life or use heart muscle cells to implement Boolean logic or run arbitrary computations in a game of _Magic: The Gathering_’.

Or in side channels, you go below bits and say, ‘these bits are only approximations to the actual flow of electricity and heat in a system; I will now proceed to measure the physical system’ etc.

*   In **social engineering/pen testing**, people see social norms and imaginary things like ‘permission’ and ‘authority’ and ‘managers’ which ‘forbid access to facilities’, but in reality, all there is, is a piece of laminated plastic or a clipboard or certain magic words spoken; the people are merely non-computerized ways of implementing rules like ‘if laminated plastic, allow in’, and if you put on a blue piece of plastic to your shirt and you incant certain words at certain times, you can walk right past the guards.⁠[⁠10⁠](https://gwern.net/unseeing#fn10)

![Image 2: US Nuclear Chain of Command: Themistocles said his infant son ruled all Greece—'Athens rules all Greece; I control Athens; my wife controls me; and my infant son controls her.' Thus, nowadays the world is controlled by whoever buys advertising time on <em>Dora the Explorer</em>.](https://gwern.net/doc/cs/security/2011-05-13-xkcd-898-chainofcommand.png)
*   Many financial or economic strategies have a certain flavor of this; [⁠Alice Maz’s _Minecraft_ economics exploits](https://www.alicemaz.com/writing/minecraft.html) strongly reminds me of ‘seeing through’, as do many clever financial trades based on careful reading of contractual minutiae or taking seriously what are usually abstracted details like ‘taking delivery’ of futures etc

*   and while we’re at it, why are **puns** so [irresistible to hackers⁠](http://www.catb.org/jargon/html/H/hacker-humor.html "‘Hacker humor’, Raymond 2003")? (Consider how omnipresent they are in _[Gödel, Escher, Bach⁠](https://en.wikipedia.org/wiki/G%C3%B6del,\_Escher,\_Bach)_ or the [Jargon File⁠](https://en.wikipedia.org/wiki/Jargon_File) or text adventures or…)

Because computers are nothing but puns on bits, and languages are nothing but puns on letters! Puns force one to drop from the abstract semantic level to the raw syntactic level of sub-words or characters, and back up again to achieve some semantic twist—they are literally hacking language.

And so on. These sorts of things can seem magical (‘how‽’), shocking (‘but—but—but that’s _cheating_!’ [the scrub](https://www.sirlin.net/articles/playing-to-win) says, who is not playing to _win_), or hilarious (in the ‘[violation of expectations⁠](https://en.wikipedia.org/wiki/Theories_of_humor#Incongruity_theory) followed by [⁠understanding⁠](https://people.idsia.ch/~juergen/creativity.html)’ theory of humor) because the abstract system _W_& our verbalizations are so familiar and useful that we quickly get trapped in our dreams of abstractions, and forget that it is merely a map and not the territory, while inevitably the map has made gross simplifications and it fails to document various paths from one point to another point which we don’t want to exist.

Indeed, these ‘backdoors’ _must_ exist unless carefully engineered away, because the high-level properties we rely on have no existence at the lower levels. If we explain things like ‘permission’ in terms of sequences of digital bits, we must at some point reach a level where the bits no longer express this ‘permission’, in the same way that if we explain ‘color’ or ‘smell’ by atoms, we must do so by eventually describing entities which do not look like they have any color nor have any smell; at some point, these properties must _disintegrate_ into brute facts like a circuit going one way rather than another.⁠[⁠11⁠](https://gwern.net/unseeing#fn11)

## [Curse of Expertise](https://gwern.net/unseeing#curse-of-expertise "Link to section: § 'Curse of Expertise'")

Perversely, the more educated you are, and the more of the map you know, the worse this effect can be, because you have more to unsee (eg. in [fiction⁠](https://gwern.net/story-of-your-life)). One must always maintain a certain contempt for [words⁠](https://gwern.net/language)&[spooks⁠](https://en.wikipedia.org/wiki/Max_Stirner#Philosophy).

The fool can walk right in because he was too ignorant to know that’s impossible. This is why atheoretical optimization processes like animals (eg. [cats engaged in⁠](https://gwern.net/fuzz-testing)[fuzz testing⁠](https://en.wikipedia.org/wiki/Fuzzing)) or [SMT solvers⁠](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) or [evolutionary AI⁠](https://arxiv.org/abs/1803.03453) are so dumb to begin with, but in the long run can be so good at surprising us and finding ‘unreasonable’ inputs or [⁠reward hacks⁠](https://gwern.net/tank#alternative-examples) (analogous to the [bias-variance tradeoff⁠](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff)): being unable to understand the map, they can’t benefit from it like we do, but they also can’t overvalue it, and, forced to explore the territory directly to get what they want, discover new things.

## [Learning To Unsee](https://gwern.net/unseeing#learning-to-unsee "Link to section: § 'Learning To Unsee'")

> I don’t even see the code. All I see is blonde, brunette, redhead.
> 
> 
> Cypher, _The Matrix_

> Whoa.
> 
> 
> Neo

To escape our semantic illusions can require a determined effort to unsee them, and use of techniques to [defamiliarize⁠](https://en.wikipedia.org/wiki/Defamiliarization) the things.

For example, you can’t find typos in your own writing without a great deal of effort because you know what it’s _supposed_ to say; so copyediting advice runs like ‘read it out loud’ or ‘print it out and read it’ or ‘wait a week’ or [recite until gibberish⁠](https://en.wikipedia.org/wiki/Semantic_satiation) or even ‘read it upside down’ (easier than it sounds). That’s the sort of thing it takes to force you to read what you actually wrote, and not what you thought you wrote. Similar tricks are used for learning drawing: a face is too familiar, so instead you can flip it in a mirror and try to copy it.

The good news is that “what has been unseen cannot be seen”, and that once one _has_ been enlightened into unseeing a system, it seems hard to slip back into the original illusion. And even a little unseeing can be a prophylactic which protects against harmful illusions.

## [External Links](https://gwern.net/unseeing#external-links "Link to section: § 'External Links'")

*   [⁠“Security Mindset and Ordinary Paranoia”⁠](https://www.lesswrong.com/posts/8gqrbnW758qjHFTrH/security-mindset-and-ordinary-paranoia); [⁠“Security Mindset and the Logistic Success Curve”⁠](https://www.lesswrong.com/posts/cpdsMuAHSWhWnKdog/security-mindset-and-the-logistic-success-curve)

*   [“How did so many _Dungeon Crawl: Stone Soup_ players miss such an obvious bug?”⁠](https://desystemize.substack.com/p/desystemize-7 "Desystemize #7")

*   [“Stargate Physics 101”⁠](https://archiveofourown.org/works/3673335)

*   [“The Line of Death”](https://textslashplain.com/2017/01/14/the-line-of-death/)

*   [⁠“Movie-Plot Threats”⁠](https://www.schneier.com/tag/movie-plot-threat-contests/)

*   [⁠“Security is Mathematics”](https://www.daemonology.net/blog/2008-03-21-security-is-mathematics.html), Colin Percival; [⁠“On Exactitude in Science”⁠](https://kwarc.info/teaching/TDM/Borges.pdf), Jorge Luis Borges

*   [“No general method to detect fraud”](https://calpaterson.com/fraud.html "No general method to detect fraud"), Cal Peterson

*   [_Red Teaming: How Your Business Can Conquer the Competition by Challenging Everything_⁠](https://www.amazon.com/Red-Teaming-Competition-Challenging-Everything/dp/1101905972), Hoffman

*   [_Baba Is You_⁠](https://en.wikipedia.org/wiki/Baba_Is_You): [⁠“No Really, There Are No Rules!”⁠](https://www.lesswrong.com/posts/gvCwotnq2cBTYqEsS/no-really-there-are-no-rules)

*   [_The City & the City_⁠](https://en.wikipedia.org/wiki/The_City_%26_the_City)

*   [Homograph attacks⁠](https://en.wikipedia.org/wiki/IDN_homograph_attack)

*   [“_Getting Over It_ Developer Reacts to 1 Minute 24 Second Speedrun”⁠](https://www.youtube.com/watch?v=dGU5_UUalPA)

*   [“The Board Game of the Alpha Nerds: Before _Risk_, before _Dungeons & Dragons_, before _Magic: The Gathering_, there was _Diplomacy_”](https://grantland.com/features/diplomacy-the-board-game-of-the-alpha-nerds/ "One writer enters international competition to play the world-conquering game that redefines what it means to be a geek (and a person)") ([WP⁠](https://en.wikipedia.org/wiki/Diplomacy_(game)); “I still don’t know whom I should have trusted, if anyone. All I know is that I felt stupid, stressed out, humiliated, and sad.”)

*   **Discussion**: Reddit: [⁠1⁠](https://www.reddit.com/r/slatestarcodex/comments/c0nqg7/people_seem_to_think_thieves_should_lockpick_or/er6huvz/), [⁠2⁠](https://www.reddit.com/r/DepthHub/comments/c0uutk/ugwern_talks_about_the_hacker_mindset_in/), [3⁠](https://www.reddit.com/r/slatestarcodex/comments/1g1lmmn/gwern_hacker_mindset_nontechnical_examples/); [Twitter⁠](https://x.com/sonyaellenmann/status/1139752544761081858)

* * *

[](https://gwern.net/unseeing#footnotes "Link to section: § ‘Footnotes’")
1.   [](https://gwern.net/unseeing#fn1 "Link to footnote 1")
‘Thinking outside the box’ can be this, but often isn’t. This is a specific pattern of reductionism, and many instances of ‘thinking outside the box’ are other patterns, like putting on another layer, or eliminating the systems in question entirely.[](https://gwern.net/unseeing#fnref1)

2.   [](https://gwern.net/unseeing#fn2 "Link to footnote 2")
[Feynman⁠](https://www.nasa.gov/history/rogersrep/v2appf.htm):

> The phenomenon of accepting for flight, seals that had shown erosion and blow-by in previous flights, is very clear. The Challenger flight is an excellent example. There are several references to previous flights; the acceptance and success of these flights are taken as evidence of safety. But erosion and blowby are not what the design expected. They are warnings that something is wrong. The equipment is not operating as expected, and therefore there is a danger that it can operate with even wider deviations in the unexpected and not thoroughly understood way. The fact that this danger did not lead to catastrophe before is no guarantee that it will not the next time, unless it is completely understood. When playing Russian roulette the fact that the first shot got off safely is little comfort for the next. The origin and consequences of the erosion and blow-by were not understood. They did not occur equally on all flights and all joints; sometimes more, and sometimes less. Why not sometime, when whatever conditions determined it were right, still more leading to catastrophe?
> 
> 
> In spite of these variations from case to case, officials behaved as if they understood it, giving apparently logical arguments to each other often depending on the “success” of previous flights…

3.   [](https://gwern.net/unseeing#fn3 "Link to footnote 3")
[⁠pg441–442](https://quod.lib.umich.edu/e/emerson/4957107.0012.001/1:15.1?rgn=div2;view=fulltext), _The complete works of Ralph Waldo Emerson: Natural history of intellect, and other papers_, Vol. 12[](https://gwern.net/unseeing#fnref3)

4.   [](https://gwern.net/unseeing#fn4 "Link to footnote 4")
“By convention sweet is sweet, bitter is bitter, hot is hot, cold is cold, color is color; but in truth there are only atoms and the void.” Incidentally, [Democritus’s⁠](https://en.wikipedia.org/wiki/Democritus) other famous quote on atomism is a pun: “For ‘Tragedy’ [_τρ**α**γωδία_] and ‘Comedy’ [_τρ**υ**γωδία_] come to be out of the same letters.” (As quoted/paraphrased by Aristotle, Book 1, [_On Generation and Corruption_⁠](https://en.wikipedia.org/wiki/On_Generation_and_Corruption); for defense of the interpretation that this is wordplay & not merely a generic observation about alphabetic writing, see [West 1969⁠](https://gwern.net/doc/philosophy/ontology/1969-west.pdf).)[](https://gwern.net/unseeing#fnref4)

5.   [](https://gwern.net/unseeing#fn5 "Link to footnote 5")
A fictional example from _[Ender’s Game⁠](https://en.wikipedia.org/wiki/Ender%27s\_Game)_ is worth noting: if victory in Battle School is defined by 4 soldiers at the corner of the enemy gate & someone passing through, then why not—shades of [Eurisko⁠](https://en.wikipedia.org/wiki/Eurisko)—skip fighting entirely & go straight for the gate?[](https://gwern.net/unseeing#fnref5)

6.   [](https://gwern.net/unseeing#fn6 "Link to footnote 6")
pg356 of [_⁠A Burglar’s Guide to the City_](https://burglarsguide.com/), Geoff Manaugh 2016:

> [Schatz’s⁠](https://en.wikipedia.org/wiki/Andy_Schatz) exhortation to [players⁠](https://en.wikipedia.org/wiki/Monaco:_What%27s_Yours_Is_Mine) to move _against_ the architecture, not with it, to uncover a scene’s possible crimes, is useful not only in the world of games. Ignoring the paths laid out by architects and even remaking a space from within are some of the most fundamental ways in which burglars misuse the built environment…In one of the most interesting moments in [Bill Mason’s⁠](https://en.wikipedia.org/wiki/Bill_Mason_(jewel_thief))[memoir⁠](https://www.amazon.com/Confessions-Master-Jewel-Thief-Mason/dp/0375760717 "_Confessions of a Master Jewel Thief_, Mason 2005"), he sees that architecture can be made to do what he wants it to do; it’s like watching a character in _Star Wars_ learn to use the Force.
> 
> 
> …he explains that his intended prize was locked inside a room whose door was too closely guarded for him to slip through. Then he realizes the obvious: he has been thinking the way the hotel wanted him to think—the way the architects had hoped he would behave—looking for doors and hallways when he could simply carve a new route where he wanted it. The ensuing realization delights him. “Elated at the idea that I could cut my own door right where I needed one,” he writes, Mason simply breaks into the hotel suite adjacent to the main office. There, he flings open the closet, pushes aside the hangers, and cuts his way from one room into the other using a drywall knife. In no time at all, he has cut his “own door” through to the manager’s office, where he takes whatever he wants—departing right back through the very “door” he himself made. It is architectural surgery, pure and simple.
> 
> 
> Later, Mason actually mocks the idea that a person would remain reliant on doors, making fun of anyone who thinks burglars, in particular, would respect the limitations of architecture. “_Surely if someone were to rob the place_,” he writes in all italics, barbed with sarcasm, “_they’d come in as respectable people would, through the door provided for the purpose. Maybe that explains why people will have 4 heavy-duty locks on a solid oak door that’s right next to a glass window_.” People seem to think they should lock-pick or kick their way through solid doors rather than just take a $14$10 2016 drywall knife and carve whole new hallways into the world. Those people are mere slaves to architecture, spatial captives in a world someone else has designed for them.
> 
> 
> Something about this is almost unsettlingly brilliant, as if it is _nonburglars_ who have been misusing the built environment this whole time; as if it is nonburglars who have been unwilling to question the world’s most basic spatial assumptions, too scared to think past the tyranny of architecture’s long-held behavioral expectations…Because doors are often the sturdiest and most fortified parts of the wall in front of you, they are a distraction and a trap. By comparison, the wall itself is often more like tissue paper, just drywall and some 2×4s, without a lock or a chain in sight. Like clouds, apartment walls are mostly air; seen through a burglar’s eyes, they aren’t even there. Cut a hole through one and you’re in the next room in seconds.

7.   [](https://gwern.net/unseeing#fn7 "Link to footnote 7")
Particularly in office buildings, ‘ceilings’ are more of [a suggestion⁠](https://en.wikipedia.org/wiki/Dropped_ceiling) than a structure; in many other buildings, like data centers, so are [the floors⁠](https://en.wikipedia.org/wiki/Raised_floor).[](https://gwern.net/unseeing#fnref7)

8.   [](https://gwern.net/unseeing#fn8 "Link to footnote 8")
Stage magician [Teller⁠](https://en.wikipedia.org/wiki/Teller_(magician)), of [Penn & Teller⁠](https://en.wikipedia.org/wiki/Penn_%26_Teller), puts this well in interviews: what makes stage magic work is _hard work_. “Magic” is spending more effort than any reasonable man would. (Therefore, all magic depends on the unreasonable man.)

Teller 2012 14ya, [“Teller Reveals His Secrets: The smaller, quieter half of the magician duo Penn & Teller writes about how magicians manipulate the human mind”⁠](https://www.smithsonianmag.com/arts-culture/teller-reveals-his-secrets-100744801/):

> I think you’ll see what I mean if I teach you a few principles magicians employ when they want to alter your perceptions…Make the secret a lot more trouble than the trick seems worth. You will be fooled by a trick if it involves more time, money and practice than you (or any other sane onlooker) would be willing to invest. My partner, Penn, and I once produced 500 live cockroaches from a top hat on the desk of talk-show host [David Letterman⁠](https://en.wikipedia.org/wiki/David_Letterman). To prepare this took weeks. We hired an entomologist who provided slow-moving, camera-friendly cockroaches (the kind from under your stove don’t hang around for close-ups) and taught us to pick the bugs up without screaming like preadolescent girls. Then we built a secret compartment out of foam-core (one of the few materials cockroaches can’t cling to) and worked out a devious routine for sneaking the compartment into the hat. More trouble than the trick was worth? To you, probably. But not to magicians.

Or in his [⁠Huttson 2015 11ya interview](http://www.magicalthinkingbook.com/2015/07/teller-of-penn-teller-on-explaining-magic-tricks/):

> **Matt**: So why don’t you explain all your tricks?
> 
> 
> **Teller**: Because the short explanation—the explanation that you’d have to do during a theatrical or TV performance—is dull and no fun. The greatest secret to making a deceptive piece of magic is you do it by the ugliest possible means. It’s complex, it’s unromantic, it’s unclever.
> 
> 
> Because there are no big secrets. There is no safe full of magic secrets somewhere. [Jim Steinmeyer⁠](https://en.wikipedia.org/wiki/Jim_Steinmeyer) said he thinks most of the public believes there’s a big safe that contains all the magic secrets. The biggest job for a magician, he says, is to conceal the fact that that safe is empty. Because every magic secret is just a minor modification of something that you fully understand in everyday life.
> 
> 
> Take ‘suspending something with a thread’, for example. Everybody’s not been able to see a piece of a thread when they were trying to put it through a needle. What makes it difficult to find is lighting and background. If a magician’s using a thread on stage, say, to levitate a ball, he must use lighting and background to conceal the thread. There’s no obscure secret in that. You learned that playing in your grandmother’s sewing box.
> 
> 
> Every magic ‘secret’ is hiding in plain sight in the everyday world. It’s not news, and eminently drab.

9.   [](https://gwern.net/unseeing#fn9 "Link to footnote 9")
[Houdini’s trick of Sir Arthur Conan Doyle⁠](https://gwern.net/doc/psychology/cognitive-bias/2006-polidoro-houdinisimpossibledemonstration.html) exemplifies these strategies.

No _reasonable person_ would expect Houdini to renovate an entire room just for a trick, to have learned a [steganographic⁠](https://en.wikipedia.org/wiki/Steganographic) code to communicate the phrase Doyle wrote on a piece of phrase to the assistant without Doyle noticing, or the assistant to manipulate a magnetic pole behind a small suspended slate board, hiding it in the viewers’ _precise_ blind spot in order to make it appear as if the chalk were hovering in mid-air & writing by itself. No reasonable person would go to such efforts to fool you. Therefore, reasonable people are fooled by Houdini’s trick.

Doyle, being a merely reasonable man, did not expect any of that; and disbelieved Houdini’s statement it was merely a trick. But Doyle should have remembered Hume’s dictum: which is more likely—witnessing the paranormal, or that [somewhere in the wide world⁠](https://gwern.net/littlewood) there was a man as cunning, careful, & compulsive as Houdini? The latter!

[Olson &Raz 2020⁠](https://gwern.net/doc/psychedelic/lsd/2020-olson-2.pdf) give further examples, and demonstrate how this can be useful for running psychology experiments.[](https://gwern.net/unseeing#fnref9)

10.   [](https://gwern.net/unseeing#fn10 "Link to footnote 10")
Speaking of ‘social engineering’, why was Facebook’s success in spreading from a niche of college students to much of the world by offering such superficial social networking so surprising to so many? Perhaps its success is a hint that the underlying logic of social interactions are much more abstractable than, and not as rich & subtle as, we’d prefer to think.[](https://gwern.net/unseeing#fnref10)

11.   [](https://gwern.net/unseeing#fn11 "Link to footnote 11")
[Heisenberg⁠](https://en.wikipedia.org/wiki/Werner_Heisenberg) (as quoted in [Hanson 1962⁠](https://gwern.net/doc/philosophy/ontology/1962-hanson.pdf)):

> It is impossible to explain…qualities of matter except by tracing these back to the behavior of entities which themselves no longer possess these qualities. If atoms are really to explain the origin of color and smell of visible material bodies, then they cannot possess properties like color and smell…Atomic theory consistently denies the atom any such perceptible qualities.

Hofstadter sums it up as [“Greenness disintegrates.”⁠](https://gwern.net/doc/philosophy/ontology/1981-hofstadter.pdf#page=21)[](https://gwern.net/unseeing#fnref11)

12.   [](https://gwern.net/unseeing#fn12 "Link to footnote 12")
“48. The best book on programming for the layman is _Alice in Wonderland_; but that’s because it’s the best book on anything for the layman.” —[“Epigrams on Programming”⁠](https://gwern.net/doc/cs/algorithm/1982-perlis.pdf), Perlis 1982 44ya.[](https://gwern.net/unseeing#fnref12)
