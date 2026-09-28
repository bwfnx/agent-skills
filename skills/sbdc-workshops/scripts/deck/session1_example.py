# Session 1 class file: the worked example. Copy it for a new class, rewrite the slides, keep the helpers.
# Build:  py <this file>   (writes the deck into the current folder)
import pathlib, sys
sys.path.insert(0, str(pathlib.Path.home() / ".claude" / "skills" / "sbdc-workshops" / "scripts" / "deck"))
import engine
engine.setup("https://docs.google.com/forms/d/e/1FAIpQLSdrHxAlHzmWBIHfZtOeAnl4bywdPei0Q934hxf16uWAZwKs3g/viewform")
from engine import *

# ============================ SLIDES ============================

slide("dark title", f'''
  <img class="logo r" alt="America's SBDC Maryland" src="data:image/png;base64,{LOGO}">
  <div class="title-grid">
    <div>
      <p class="eyebrow light r">Winning That Government Contracting Award &middot; Session 1 of 4</p>
      <h1 class="r">Business Development Lifecycle</h1>
      <div class="band r"></div>
      <p class="byline r">Brandon Mason &middot; Maryland Small Business Development Center<br>Monday, September 28, 2026</p>
    </div>
    <div class="qr-card r">{QR_FORM}<span>Scan now: your worksheet</span></div>
  </div>''',
  "Welcome everyone. I'm Brandon Mason with the Maryland SBDC. Over the next four sessions we walk through what it actually takes to win a government contract, from finding the opportunity to submitting a winning proposal. Today is the big picture: the full business development lifecycle. This is not theory. Everything today comes from working with hundreds of small businesses going after government work. Some of it you'll know. Some of it might change how you think about this whole process. Before we start: scan the code on screen. That's your worksheet for today.", label="Title")

slide("light scan", f'''
  <div class="scan-grid">
    <div>
      <ol class="steps">
        <li class="r"><b>Point your phone camera at the code.</b> Or click the link in the Zoom chat.</li>
        <li class="r"><b>Fill in page 1 now.</b> Name, email, business, where you are today.</li>
        <li class="r"><b>Keep the tab open.</b> We come back to it three times today.</li>
      </ol>
      <p class="url ink r">{FORM_LABEL}</p>
      <p class="fine r">When you submit at the end, the capture template and every link from today land in your inbox.</p>
    </div>
    <div class="qr-card big r">{QR_FORM}</div>
  </div>''',
  "Give them 90 seconds. Say: fill in your name and email now and keep that tab open. If you close it you start over, and no email means no follow-up and no capture template. Diane: please paste the link in the Zoom chat.",
  eyebrow="Before we start", title="Scan your worksheet")

slide("light", '''
  <ol class="agenda">
    <li class="r"><span>01</span>Where to find government opportunities</li>
    <li class="r"><span>02</span>How the government actually buys</li>
    <li class="r"><span>03</span>Revenue strategies: where you fit right now</li>
    <li class="r"><span>04</span>The 36-month capture pipeline</li>
    <li class="r"><span>05</span>The six phases of business development</li>
    <li class="r"><span>06</span>Go/No-Go: knowing when to walk away</li>
  </ol>''',
  "Here's the roadmap. This is usually more information than most people can handle in one sitting. That's fine. It all lands in your inbox after you submit the worksheet. I'd honestly recommend throwing it into NotebookLM or ChatGPT and asking it questions. That's what most of my clients do.",
  eyebrow="Today", title="What we're covering")

section("Part 1", "Finding opportunities",
  "Let's start at the beginning. Before capture strategy or proposal writing, you need to know where to actually look.")

slide("light", '''
  <div class="tiers">
    <div class="tier t1 r"><b>Federal</b><span>SAM.gov &middot; the single federal marketplace</span><em>$$$</em></div>
    <div class="tier t2 r"><b>State</b><span>eMaryland Marketplace Advantage (eMMA)</span><em>$30k+</em></div>
    <div class="tier t3 r"><b>County &amp; City</b><span>Howard, Montgomery, Prince George's, Baltimore Co., Baltimore City, Annapolis</span><em>$15k+</em></div>
  </div>
  <div class="also r"><b>Also look at:</b> subcontractor &amp; expiring-contract lists &middot; master contract award lists &middot; procurement forecasts &middot; networking, industry days, social media</div>''',
  "SAM.gov is where most people start, and that's fine. But I listed eight places and SAM.gov is one of them. Government contracting doesn't mean federal contracting. Maryland buys through eMMA. Your county buys. Your city buys. The thresholds are lower: $15k local, $30k state. If you're just starting out, look there first. Federal is where the big money is, and the big competition. Also flag procurement forecasts: agencies publish what they plan to buy next fiscal year. Most small businesses don't know these exist. Links come in the follow-up email.",
  eyebrow="Part 1 &middot; Finding opportunities", title="Where to look")

slide("light", '''
  <div class="cols2">
    <div class="card r"><p class="card-k">How they buy</p>
      <dl class="buy">
        <dt>Federal</dt><dd>Existing contract vehicles (IDIQs, GSA Schedule, SeaPort-e, OASIS+, OTAs), open solicitations on SAM.gov, DSBS for set-asides, forecasts</dd>
        <dt>State</dt><dd>eMMA for $30k+</dd>
        <dt>County / City</dt><dd>Procurement portals for $15k+</dd>
      </dl>
    </div>
    <div class="card accent r"><p class="card-k">Below ~$15k</p>
      <p class="big-line">Purchase cards.</p>
      <p>A government credit card. No formal solicitation required. If you sell something an agency needs for under ~$15k, a contracting officer can just buy it.</p>
    </div>
  </div>''',
  "The government doesn't buy like a normal customer. At the federal level most money flows through existing contract vehicles: IDIQs, GSA Schedules, OASIS+. Those are basically pre-approved lists of vendors. If you're not on one, you're either competing on an open solicitation through SAM.gov or, where a lot of my clients start, subcontracting under someone who is. Below about $15k, agencies can use purchase cards. No formal solicitation. That's worth knowing.",
  eyebrow="Part 1 &middot; Finding opportunities", title="How the government actually buys")

slide("light", '''
  <table class="compare r">
    <thead><tr><th></th><th>Government</th><th>B2B</th></tr></thead>
    <tbody>
      <tr><td>Where</td><td>Portals &amp; contract vehicles</td><td>Supplier portals, direct outreach</td></tr>
      <tr><td>Process</td><td>Formal: RFPs, RFQs, set-asides</td><td>RFPs, RFQs, traditional sales</td></tr>
      <tr><td>Timeline</td><td>Months to years</td><td>Weeks to months</td></tr>
      <tr><td>Rules</td><td>Compliance on top of everything</td><td>Fewer rules</td></tr>
      <tr><td>Relationships</td><td>Matter, within the rules</td><td>Often drive the deal</td></tr>
    </tbody>
  </table>
  <p class="takeaway r">The capture discipline works for both. Government adds compliance on top.</p>''',
  "Quick sidebar for those coming from the private sector. B2B is simpler: fewer rules, shorter timelines, more room for relationships. Some of you will do both, and the skills overlap more than you'd think. The capture discipline we're about to cover works for B2B too.",
  eyebrow="Quick comparison", title="Government vs. B2B")

section("Part 2", "Revenue strategies: where do you fit?",
  "You know where to look. Now: where do you actually fit in this ecosystem right now? That determines your strategy.")

slide("light", '''
  <div class="stairs">
    <div class="step s1 r"><p class="step-n">Strategy 1</p><h3>Sub under small</h3><p>Start here. Find a small-business prime with the contract, past performance and certifications, and offer your skills as a sub.</p></div>
    <div class="step s2 r"><p class="step-n">Strategy 2</p><h3>Prime with agencies</h3><p>When you have: federal experience, 3+ years of revenue, clearances if needed, strategic partnerships.</p></div>
    <div class="step s3 r"><p class="step-n">Strategy 3 &middot; parallel track</p><h3>Sub under large</h3><p>Large primes need small subs to hit small-business goals (often 23%+). Steady, but a smaller piece of a bigger pie.</p></div>
  </div>
  <p class="takeaway r">Know which strategy you're running <u>right now</u>.</p>''',
  "One of the most important slides in the whole series. A lot of clients want to prime on federal contracts right away. Unless you have past performance and revenue history, that's not where you start. Strategy 1 is where most begin: find a small business that has contracts and past performance and ideally doesn't have your certifications. That's your unicorn partner. Strategy 2 is where you're headed. Strategy 3 is the Lockheed play: large primes have small-business subcontracting goals and need small businesses to team with. Don't run Strategy 2 when you're still in Strategy 1 mode.",
  eyebrow="Part 2 &middot; Revenue strategies", title="Three revenue strategies")

slide("light", '''
  <div class="cols2 wide-left">
    <div>
      <p class="statement r">Early on, certifications are about <em>subcontracting</em>, not priming.</p>
      <div class="chips r"><span>8(a)</span><span>MBE</span><span>EDWOSB</span><span>SDVOSB</span><span>HUBZone</span></div>
    </div>
    <div class="card r">''' + bullets([
        "They make you the partner a prime needs",
        "SDVOSB and some others rarely see large prime awards (mostly VA)",
        "Maryland MBE matters most on state contracts",
        "The SBDC helps with certifications, free",
        "Tedious, not hard"]) + '''</div>
  </div>''',
  "Correct the misconception: certifications are not a golden ticket. What they do is make you attractive as a subcontractor. That unicorn partner is looking for certifications they don't have. Yes, there are 8(a), HUBZone, SDVOSB set-asides. But early on the value is in teaming. Maryland MBE is specifically valuable for state procurements because state contracts carry MBE participation goals. We help with all of this for free.",
  eyebrow="Part 2 &middot; Revenue strategies", title="Certifications = teaming leverage")

checkpoint("Section A", "Where do you fit?",
  "Tap Next to Section A. Which strategy are you running right now, and which one agency or buyer would you focus on first?",
  "Give them two minutes. Ask for one or two volunteers to say their answer out loud or drop it in the Zoom chat. React to one: is that strategy honest for where they are today?")

section("Part 3", "The 36-month capture pipeline",
  "This is the part that changes how you think about government contracting. Here's the real timeline.")

slide("light", '''
  <div class="timeline r">
    <div class="tl-bar">
      <div class="tl-seg a"><b>Positioning &amp; research</b><span>Months 1&ndash;12</span></div>
      <div class="tl-seg b"><b>Capture &amp; teaming</b><span>Months 12&ndash;24</span></div>
      <div class="tl-seg c"><b>Pre-proposal &amp; proposal</b><span>Months 24&ndash;36</span></div>
    </div>
    <div class="tl-rfp"><span>RFP released<br><small>~month 28&ndash;30</small></span></div>
    <div class="tl-award">Award</div>
  </div>
  <p class="statement center r">You will lose if you wait until the RFP is released.</p>''',
  "Let that sink in. Three years. Most clients think they'll find an RFP this week, write the proposal next month and win by the end of the quarter. That's not how this works. Winners start two to three years before the solicitation drops: building relationships, positioning, shaping requirements. By the time the RFP hits the street, the winner is usually already decided in practice. Can you win something you just found? It happens. But the odds are dramatically better when you've been working the pipeline.",
  eyebrow="Part 3 &middot; The pipeline", title="The real timeline: 36 months")

slide("light", '''
  <div class="cols2">
    <div class="stat r"><p class="stat-n">150+</p><p class="stat-l">hours to write your first federal proposal</p></div>
    <div>
      <div class="curve r">
        <div><b>Proposal #1</b><span style="width:100%"></span><em>150+ hrs</em></div>
        <div><b>Proposal #2</b><span style="width:50%"></span><em>about half</em></div>
        <div><b>Proposal #3</b><span style="width:25%"></span><em>about a quarter</em></div>
      </div>
      ''' + bullets(["Processes and templates make every cycle faster",
                     "One agency or customer speeds it up even more",
                     "3 weeks on a proposal you miss the deadline for = lost opportunity"]) + '''
    </div>
  </div>''',
  "The good news: the first one is brutal, 150 hours minimum. But once you've done one you have templates, boilerplate, a reusable compliance matrix, past performance narratives. The second takes half the time, the third a quarter. Pick a lane: don't chase DOD, HHS and the State of Maryland at once. And I've had clients spend three weeks on a proposal and miss the deadline. That's opportunity cost. Go/No-Go later today helps with that.",
  eyebrow="Part 3 &middot; The pipeline", title="The first proposal is the hardest")

slide("light", '''
  <div class="cols2">
    <div class="capstmt r">
      <p class="card-k">Capability statement &middot; one page</p>
      <div class="cs"><div class="cs-h">Company &middot; contact</div><div class="cs-r"><span>Core competencies</span><span>Differentiators</span></div><div class="cs-r"><span>Past performance</span><span>NAICS &middot; certs &middot; UEI/CAGE</span></div></div>
      <p class="fine">Have several versions, one per buyer or NAICS. <b>Pro tip:</b> image-search &ldquo;Capability Statement [your NAICS]&rdquo; for real examples.</p>
    </div>
    <div class="card r"><p class="card-k">Buyers will Google you</p>''' + bullets([
        "No website = you don't exist",
        "No social media = you don't exist",
        "Neglected social media = red flag",
        "It doesn't have to be fancy. It has to exist and look professional."], "checks") + '''</div>
  </div>''',
  "Two things that trip people up. Your cap statement is your one-page resume for government buyers: NAICS codes, certifications, past performance, differentiators, contact info. One page. Beltway firms keep 30 to 60 versions ready to email. The trick: Google image search Capability Statement plus your NAICS code, and study the layouts. Don't copy, study. And yes, government buyers Google you. A 2005 website or a LinkedIn untouched for a year is a problem.",
  eyebrow="Part 3 &middot; The pipeline", title="Your marketing collateral")

section("Part 4", "The six phases of business development",
  "Now the meat of it. Six phases. This is the framework large companies use, and I'll show you how to scale it down.")

slide("light", '''
  <div class="phases">
    <div class="ph pre r"><span>1</span>Long-term positioning</div>
    <div class="ph pre r"><span>2</span>Opportunity assessment</div>
    <div class="ph pre r"><span>3</span>Capture team development</div>
    <div class="ph post r"><span>4</span>Pre-proposal preparation</div>
    <div class="ph post r"><span>5</span>Proposal development</div>
    <div class="ph post r"><span>6</span>Post-submittal activities</div>
  </div>
  <div class="ph-legend r"><span class="pre">Capture &middot; before the RFP</span><span class="post">Proposal &middot; after the RFP</span></div>''',
  "Six phases. Large companies have entire departments for each. You probably don't, and that's okay. What matters is you understand each phase well enough to do a reasonable version at your scale. Don't memorize this. It's in the follow-up.",
  eyebrow="Part 4 &middot; Six phases", title="The business development lifecycle")

slide("light phase", '<div class="phase-tag r">1</div>' + bullets([
    "Identify your strategic markets: where do you want to play?",
    "Assess market direction and upcoming opportunities",
    "Benchmark your capabilities: where are your gaps?",
    "Build strategic alliances: teaming partners, mentors, primes",
    "Set criteria to prioritize (you can't chase everything)",
    "Start marketing: industry days, relationships, get known"], "checks"),
  "The phase most small businesses skip entirely, and arguably the most important. For you this looks like: pick your NAICS codes, pick 2 or 3 agencies, attend their industry days, find the small business liaison officer, start building relationships. Look at who's winning in your space and figure out how you complement them. As soon as I know your constraints, I can move forward. Same here. Pick a lane.",
  eyebrow="Phase 1 &middot; Capture", title="Long-term positioning")

slide("light phase", '''<div class="phase-tag r">2</div>
  <div class="cols2 wide-left">''' + bullets([
    "Gather preliminary customer intelligence",
    "Attend industry briefings and pre-solicitation conferences",
    "Understand basic requirements; identify probable competitors",
    "Early analysis: is this a fit? can you compete?",
    "<b>Make the Bid/No-Bid decision</b>",
    "If Go: assign a capture manager (even if it's you)"]) + '''
    <div class="funnel r"><div>Every opportunity</div><div>Bid / No-Bid filter</div><div>Qualified</div></div>
  </div>''',
  "Phase 2 is where you find a specific opportunity and decide whether to pursue it. Intelligence gathering: who's the incumbent, how long have they held it, estimated value, set-aside, do you have the certs and past performance. Clients who skip this and write the day the RFP drops are how you waste 150 hours.",
  eyebrow="Phase 2 &middot; Capture", title="Opportunity assessment")

slide("light phase", '''<div class="phase-tag r">3</div>
  <div class="cols2">
    <div class="roles r">
      <div><b>Capture manager</b><span>owns the strategy and the win</span></div>
      <div><b>Proposal manager</b><span>owns the document and process</span></div>
      <div><b>Solution architect / SME</b><span>owns the technical approach</span></div>
      <div><b>Pricing strategist</b><span>owns the numbers</span></div>
      <div><b>Business development</b><span>owns the relationship</span></div>
      <p class="fine">In a small business, one person may fill 2 or 3 of these.</p>
    </div>''' + bullets([
    "Establish customer contacts",
    "Gather and analyze program intelligence",
    "Write the capture strategy and plan",
    "Set the bid and proposal budget",
    "Start teaming and subcontractor relationships",
    "Define your winning price"]) + '</div>',
  "In a large company this is 15 to 20 people. For most of you it's 2 or 3, or just you. What matters is the functions get covered. The capture strategy answers: why will the customer pick us? It has to be specific. Not we're the best, but three past performance examples on this exact work, 15% below the incumbent's likely price, a local team that starts day one. This is also when you find the unicorn partner.",
  eyebrow="Phase 3 &middot; Capture", title="Capture team development")

slide("light phase", '''<div class="phase-tag post r">4</div>
  <div class="cols2">''' + bullets([
    "Proposal strategy, tasks, budget and schedule",
    "Work breakdown structure (WBS)",
    "Teaming and subcontractor statements of work",
    "Outline from Sections L and M of the RFP",
    "Reuse what you can from past proposals",
    "Draft the Executive Summary; hold a kickoff"]) + '''
    <div class="keyouts r"><p class="card-k">Key outputs</p><div class="ko">Compliance matrix</div><div class="ko">Storyboards</div><p class="fine">Map Section L (instructions) and Section M (evaluation) before you write a word. Template in Session 3.</p></div>
  </div>''',
  "Now you shift from should we do this to how will we do this. Biggest mistake: people start writing immediately. Don't. Outline first. Map Section L, the preparation instructions, and Section M, the evaluation criteria. Build the compliance matrix. Then write. A storyboard is a one-page visual outline per section: heading, key message, theme, main graphic, supporting points. At minimum, do one for the Executive Summary and the technical approach.",
  eyebrow="Phase 4 &middot; Proposal", title="Pre-proposal preparation")

slide("light phase", '''<div class="phase-tag post r">5</div>
  <div class="colorflow r">
    <div class="cf write">Write</div><i></i>
    <div class="cf pink">Pink team<small>Is the story there?</small></div><i></i>
    <div class="cf write">Revise</div><i></i>
    <div class="cf red">Red team<small>Compliant? Persuasive? Priced right?</small></div><i></i>
    <div class="cf write">Revise</div><i></i>
    <div class="cf gold">Gold team<small>Legal, cost, management sign-off</small></div><i></i>
    <div class="cf submit">Submit</div>
  </div>
  <p class="statement center r">Never submit a proposal that only its writers have read.</p>''',
  "This is where the work happens. Pink team is your first-draft review: does this tell a winning story? Red team is the hard one: bring in someone who hasn't been writing, ideally someone who has evaluated proposals, and let them tear it apart. Gold team is final legal, cost and management sign-off. Small business can combine pink and red. But get at least one external review. Fresh eyes catch what you can't see. More in Session 2 on Wednesday.",
  eyebrow="Phase 5 &middot; Proposal", title="Proposal development")

slide("light phase", '''<div class="phase-tag post r">6</div>
  <div class="cols2 wide-right">''' + bullets([
    "Keep all proposal documentation organized",
    "Answer clarification requests",
    "Orals, demos, discussions",
    "Revalidate pricing if asked",
    "Negotiate if selected",
    "Run lessons learned"]) + '''
    <div class="callout r"><p>Always request a debrief.</p><span>Win or lose.</span></div>
  </div>''',
  "Proposal's in. Don't disband the team: the government may come back with questions or ask for orals. And always ask for a debrief. If you win, it tells you what they liked. If you lose, it tells you exactly why. Clients who take debriefs seriously improve their win rate dramatically. Lessons learned is how 150 hours becomes a fraction of that.",
  eyebrow="Phase 6 &middot; Proposal", title="Post-submittal activities")

section("Part 5", "Go/No-Go: the decision that saves you",
  "One of the most important skills in government contracting: knowing when to walk away.")

slide("light", '''
  <div class="four r">
    <div><b>Customer</b><span>Do you know them? Have you engaged? Do you understand their pain?</span></div>
    <div><b>Competition</b><span>Who else is bidding? Who's the incumbent, and are they happy with them?</span></div>
    <div><b>Capabilities</b><span>Can you do the work? Do you have past performance on this type of contract?</span></div>
    <div><b>Cost</b><span>Can you win on price? Do you understand the pricing structure?</span></div>
  </div>
  <p class="takeaway r">Weak on two or more? Red flag.</p>''',
  "The Four C's: Customer, Competition, Capabilities, Cost. Weak on two or more is a red flag. The one people skip most is Competition. If the incumbent has done the work for 10 years and the customer's happy, your pWin is low unless you bring something genuinely different. The one people overestimate is Capabilities. Similar work is not the same as federal past performance on the same type of contract. Be honest.",
  eyebrow="Part 5 &middot; Go/No-Go", title="Probability of win: the Four C's")

checkpoint("Section B", "Score one opportunity",
  "Section B: name one opportunity you're watching and rate it 1 to 5 on Customer, Competition, Capabilities and Cost. Then make the call: Go or No-Go.",
  "Three minutes. Then ask: who scored themselves below 3 on two or more? That's the conversation. Anyone without an opportunity yet: score the buyer you named in Section A.")

slide("light", '''
  <div class="gng">
    <div class="no r"><h3>No-Go if you</h3>''' + bullets([
        "Lack expertise in the work",
        "Have a business or ethical conflict",
        "Would stretch resources too thin",
        "Don't believe it's real or attainable",
        "Don't have time for an <em>excellent</em> proposal"]) + '''</div>
    <div class="go r"><h3>Go if you</h3>''' + bullets([
        "Have expertise in the work",
        "Have resources to perform",
        "Have time for an excellent proposal",
        "Can submit a letter of intent if required"]) + '''</div>
  </div>
  <p class="takeaway r">Weigh probability of win, cost to propose, and estimated profit.</p>''',
  "Be selective. It feels counterintuitive when you're breaking in, but chasing everything is how you burn out and win nothing. The best contractors might look at 50 and bid 5. No-Go is as important as Go. If you don't have time for an excellent proposal, not a good one, that's a No-Go. Protect the work you have while pursuing new work.",
  eyebrow="Part 5 &middot; Go/No-Go", title="Be selective")

slide("light", '''
  <div class="split r">
    <div class="half cap"><p>Phases 1&ndash;3</p><h3>Capture</h3><span>Everything before the RFP</span></div>
    <div class="divider"><span>RFP</span></div>
    <div class="half prop"><p>Phases 4&ndash;6</p><h3>Proposal</h3><span>Everything after</span></div>
  </div>
  <p class="statement center r">Most small businesses only do proposal. Consistent winners do both.</p>''',
  "Credit where it's due: the six phases are adapted from the Shipley process, the industry standard. If you want to go deeper, Shipley's materials are excellent. The key takeaway ties back to the 36-month pipeline. Capture is everything before the RFP drops. Proposal is everything after. Stop being reactive. Start being proactive.",
  eyebrow="Industry standard &middot; Shipley", title="Capture before, proposal after")

slide("light", '''
  <div class="tiles">
    <div class="r"><span>1</span><b>Look beyond SAM.gov</b>State, county and city have lower barriers</div>
    <div class="r"><span>2</span><b>Know your strategy</b>Subbing, priming, or both. Be honest.</div>
    <div class="r"><span>3</span><b>Think in 36 months</b>Winners start years before the RFP</div>
    <div class="r"><span>4</span><b>Build templates now</b>The first proposal is the hardest</div>
    <div class="r"><span>5</span><b>Be selective</b>Not every opportunity is yours</div>
    <div class="r"><span>6</span><b>Always debrief</b>Win or lose</div>
  </div>''',
  "Six things. If you remember nothing else: think in 36-month cycles, know your revenue strategy, and be selective.",
  eyebrow="Today", title="What to remember")

slide("light", f'''
  <div class="cols2">
    <div class="card r"><p class="card-k">Wednesday, Sept 30 &middot; 10:00 a.m. &middot; Session 2</p>
      <h3 class="next-h">Team roles &amp; responsibilities</h3>''' + bullets([
        "Who does what on a proposal team",
        "Scaling roles when you're one to three people",
        "Running color team reviews",
        "When to bring in outside help"]) + f'''</div>
    <div class="submit-card r">
      <p class="eyebrow light">Worksheet &middot; Section C</p>
      <h3>Write your one step, then submit.</h3>
      <p>Your inbox gets: this deck with notes, the capture management template, and links to SAM.gov, eMMA, county portals and forecasts.</p>
      <div class="mini-qr">{QR_FORM}</div>
    </div>
  </div>''',
  "Wednesday: team roles. If you're thinking I don't have a team, that's fine, we cover one- to three-person operations. Now: Section C, write the one capture step you'll take this month, tick what you want, then the last page and Submit. That's what triggers the follow-up with the deck, the capture template and all the links. Throw it into NotebookLM and ask it questions.",
  eyebrow="What's next", title="Submit your worksheet")

slide("dark title close", f'''
  <img class="logo r" alt="America's SBDC Maryland" src="data:image/png;base64,{LOGO}">
  <div class="title-grid">
    <div>
      <h1 class="r">Questions?</h1>
      <div class="band r"></div>
      <p class="byline r">Brandon Mason &middot; Maryland SBDC<br>bwmason@umd.edu</p>
      <p class="byline small r">No-cost, one-on-one consulting. Register as an SBDC client: {SIGNUP_LABEL}</p>
    </div>
    <div class="qr-card r">{QR_SIGNUP}<span>Register for 1:1 advising</span></div>
  </div>
  <p class="sba r">Funded in part through a Cooperative Agreement with the U.S. Small Business Administration. All opinions, conclusions, and/or recommendations expressed herein are those of the author(s) and do not necessarily reflect the views of the SBA. Reasonable accommodations for persons with disabilities will be made if requested at least two weeks in advance.</p>''',
  "Open it up. Let the conversation go where it needs to go. Remind them to submit the worksheet if they haven't.", label="Questions")

engine.render(pathlib.Path.cwd() / "Business-Development-Lifecycle.html",
              title="Business Development Lifecycle",
              footer="Session 1 &middot; Business Development Lifecycle")
