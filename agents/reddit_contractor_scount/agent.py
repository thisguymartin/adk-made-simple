import os
import random
from google.adk.agents import Agent
from dotenv import load_dotenv
import praw
from praw.exceptions import PRAWException

# Load environment variables from the root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def get_mock_reddit_contractor_news(subreddit: str) -> dict[str, list[str]]:
    """
    Simulates fetching top post titles from contractor and HVAC subreddits.

    Args:
        subreddit: The name of the subreddit to fetch news from (e.g., 'hvac', 'contractors').

    Returns:
        A dictionary with the subreddit name as key and a list of
        mock post titles as value. Returns a message if the subreddit is unknown.
    """
    print(f"--- Tool called: Simulating fetch from r/{subreddit} ---")
    mock_titles: dict[str, list[str]] = {
        "hvac": [
            "R-32 refrigerant transition timeline - Equipment compatibility and training requirements: Major manufacturers phasing out R-410A by 2026, requiring technician recertification for A2L refrigerants. New leak detection requirements, updated brazing techniques, and storage protocols. Equipment costs 15-20% higher but improved efficiency ratings.",
            "Heat pump rebates and tax credits: Federal and state incentive programs for 2025: IRA tax credits up to $2,000 for heat pump installations, plus state rebates varying $500-$3,000. Income-qualified programs offering point-of-sale discounts. Contractor pre-approval processes and paperwork requirements creating administrative burden but driving demand.",
            "Smart thermostat integration: Wi-Fi 6E and Matter protocol compatibility issues: Legacy systems struggling with new protocols, requiring gateway devices or complete replacement. Customer complaints about connectivity dropouts during peak usage. Compatibility matrices becoming essential for proper system design and avoiding callbacks.",
            "Ductless mini-split systems: Market demand surge in retrofit applications: 40% increase in residential installations driven by energy costs and zoning needs. Challenges with refrigerant line routing in finished spaces, electrical requirements for multiple indoor units, and customer education on proper operation and maintenance.",
            "Indoor air quality focus: UV-C sterilization and advanced filtration upgrades: Post-pandemic awareness driving demand for MERV 13+ filters, bipolar ionization, and UV systems. Integration challenges with existing ductwork, increased static pressure concerns, and explaining ROI to cost-conscious customers.",
            "Commercial HVAC automation: IoT sensors and predictive maintenance ROI: Building management systems generating terabytes of data, requiring new diagnostic skills. Sensor calibration and network security concerns. Demonstrating 20-30% maintenance cost reduction through predictive analytics, but initial setup complexity deterring smaller commercial clients.",
            "Geothermal heat pump installations: Permitting challenges and soil conditions: Local authorities lacking expertise for permit approval, requiring geological surveys and thermal conductivity testing. Loop field sizing calculations becoming more critical with energy efficiency requirements. Higher upfront costs offset by 50-year system life and stable operating costs.",
        ],
        "contractors": [
            "AI project estimation tools: Which software is actually saving time and money?: Tools like Stack, PlanSwift AI, and Buildertrend reducing takeoff time by 60-80%. Learning curve averaging 2-3 months for full adoption. Integration with existing accounting systems creating workflow challenges but improving bid accuracy and reducing change orders by 25%.",
            "Gen Z workforce: Adapting management styles for younger skilled trades workers: Digital-native workers expecting real-time feedback, flexible scheduling, and career advancement clarity. Traditional apprenticeship models evolving to include video training, gamification elements, and mentorship pairing. Higher starting wage expectations but faster skill acquisition through technology.",
            "Supply chain resilience: Building relationships with multiple material suppliers: Single-source dependencies causing 2-6 week project delays. Contractors developing 3-4 supplier relationships per material category. Local supplier partnerships becoming competitive advantage. Material cost fluctuations requiring dynamic pricing models and customer education.",
            "Digital payments: Contactless transactions and automated invoicing systems: Customer preference shifting to digital payments, reducing check processing time from days to hours. Integration with accounting software streamlining cash flow management. Security concerns requiring PCI compliance training and updated payment processing agreements.",
            "Licensing reciprocity updates: Multi-state contractor certification programs: Interstate compacts simplifying licensing for contractors working across state lines. Continuing education requirements varying by state creating compliance complexity. Specialty trade certifications gaining importance for commercial work and insurance rates.",
            "Liability insurance costs: How recent litigation trends affect premium rates: Material defect lawsuits increasing premiums 15-25% annually. Cyber liability coverage becoming mandatory for contractors handling customer financial data. Documentation requirements intensifying for claims defense, requiring systematic project photography and communication records.",
            "Sustainable building practices: Green certifications that clients actually value: LEED, Energy Star, and local green building programs driving premium pricing 5-15%. Material sourcing documentation and waste reduction protocols adding administrative overhead. Customer education needed to justify additional costs and timeline extensions.",
        ],
        "homeimprovement": [
            "Smart home security integration: Ring vs ADT vs DIY system comparisons: Professional monitoring costs $20-60/month with varying contract terms. DIY systems requiring customer technical support but offering flexibility. Integration challenges with existing doorbell wiring and Wi-Fi coverage. Privacy concerns affecting customer adoption rates.",
            "Aging in place modifications: Universal design trends for baby boomers: 10,000 Americans turning 65 daily driving demand for accessibility improvements. Zero-step entries, 36-inch doorways, and curbless showers becoming standard requests. ADA compliance knowledge becoming competitive advantage. Insurance and Medicare reimbursement navigation required.",
            "Energy efficiency upgrades: Heat pump water heaters and induction cooktop conversions: Federal tax credits covering 30% of heat pump water heater costs through 2032. Electrical panel upgrades often required for induction cooktops, adding $2,000-4,000 to project costs. Customer education needed on operational differences and energy savings calculations.",
            "Outdoor living spaces: Composite decking and pergola material innovations: Composite material costs 2-3x traditional lumber but 25-year warranties driving adoption. Fastener compatibility and thermal expansion considerations critical for proper installation. Pergola kit systems simplifying installation but requiring structural engineering for wind load compliance.",
            "Home office conversions: Basement and garage transformation ideas: Remote work permanence driving demand for dedicated office spaces. Moisture control, insulation upgrades, and egress window requirements adding complexity. Electrical and HVAC system extensions required. Permit requirements varying significantly by jurisdiction.",
            "Water damage prevention: Smart leak detectors and automatic shutoff valves: Insurance discounts 5-15% for whole-house leak detection systems. Integration with existing plumbing requiring retrofitting challenges. Battery backup systems and cellular connectivity ensuring operation during power outages. Customer training needed for system maintenance and alert response.",
            "Resale value focus: Which 2025 renovations provide best return on investment: Kitchen remodels returning 70-80% of investment, bathroom renovations 60-70%. Energy efficiency improvements adding 4-6% to home value. Neutral design choices and quality materials specification crucial for resale appeal. Market analysis by region showing significant variation in buyer preferences.",
        ],
        "electricians": [
            "EV infrastructure boom: Level 2 charger installations and electrical panel upgrades: 240V, 40-50 amp circuits becoming standard residential requirement. Panel upgrades needed in 60% of installations, adding $1,500-3,000 to project costs. Permit requirements and utility coordination varying by jurisdiction. Load management systems preventing costly service upgrades.",
            "Solar + battery storage systems: Grid-tied vs off-grid configuration challenges: Battery storage costs dropping 20% annually but still representing 40-60% of system cost. Grid interconnection requirements and utility approval processes taking 2-6 months. NEC 2023 rapid shutdown requirements affecting system design and component selection.",
            "Smart panel technology: Real-time energy monitoring and circuit-level control: Panels with integrated monitoring reducing installation complexity but requiring Wi-Fi configuration and app setup. Customer education needed for energy usage optimization. Integration with time-of-use utility rates enabling automated load shifting for cost savings.",
            "Apprenticeship program updates: Community college partnerships and certification paths: 4-year apprenticeships combining classroom and field experience. NCCER certification becoming industry standard. Shortage of qualified instructors limiting program capacity. Starting wages $18-22/hour with guaranteed progression schedules attracting career changers.",
            "Arc fault breaker requirements: New installation standards and troubleshooting: NEC 2023 expanding AFCI requirements to all 120V circuits in dwelling units. Nuisance tripping issues with older wiring requiring systematic troubleshooting approaches. Compatibility testing with LED lighting and electronic devices preventing callbacks.",
            "Data center electrical work: High-demand specialty niche opportunities: Hyperscale data centers requiring 480V three-phase distribution and redundant power systems. Specialized training in UPS systems, generator paralleling, and power quality monitoring. Security clearance requirements for government and financial sector facilities adding complexity but premium pricing.",
            "LED retrofit projects: Dimmer compatibility and flicker-free lighting solutions: Driver compatibility with existing dimmer switches requiring systematic replacement planning. Flicker-sensitive applications in video production and healthcare requiring specialized LED products. Color temperature consistency and CRI requirements affecting product selection and costs.",
        ],
        "plumbing": [
            "Water filtration systems: Whole-house vs point-of-use installation strategies: Whole-house systems requiring backwash drain connections and electrical supply for controller units. Point-of-use systems offering targeted treatment but requiring multiple installation points. Filter replacement scheduling and customer education critical for system performance and warranty compliance.",
            "Smart water heaters: Wi-Fi connectivity and energy usage optimization features: Heat pump water heaters with smart controls reducing energy costs 60-70% but requiring specific installation environments. Connectivity setup and app configuration becoming standard service offering. Diagnostic capabilities reducing service call frequency but requiring technician training on digital interfaces.",
            "Greywater recycling systems: Permitting requirements and homeowner education: State regulations varying significantly, with California leading adoption through rebate programs. Laundry-to-landscape systems requiring specific detergent types and plant selection. Health department approvals and inspection requirements adding timeline complexity to installations.",
            "Pipe inspection technology: 4K cameras and AI-powered diagnostic software: Camera systems with real-time defect identification reducing diagnostic time 40-50%. Cloud-based reporting enabling instant customer documentation and estimate generation. Equipment costs $15,000-30,000 requiring service volume analysis for ROI justification.",
            "Low-flow fixture regulations: Compliance requirements and customer satisfaction: Federal standards limiting flow rates while maintaining performance expectations. Customer complaints about reduced water pressure requiring education on aerator technology and system design. Premium fixture lines offering performance at regulated flow rates commanding higher margins.",
            "Radiant floor heating: Retrofit applications in existing homes with concrete slabs: Electric mat systems enabling retrofit installations without major floor modifications. Thermostat zoning and programmable controls optimizing energy usage. Integration with existing HVAC systems requiring load calculations and electrical planning for proper operation.",
            "Emergency service scheduling: Digital dispatch systems and customer communication: GPS tracking and automated scheduling reducing response times 20-30%. Real-time customer communication through text and app notifications improving satisfaction scores. After-hours premium pricing strategies and technician compensation models balancing profitability with customer service.",
        ],
        "construction": [
            "3D printing applications: Concrete printing for residential foundation work: Large-scale 3D printers reducing foundation construction time 50-70% while improving accuracy. Material limitations requiring specialized concrete mixes and reinforcement strategies. Permitting challenges as building codes adapt to new construction methods and inspection protocols.",
            "Modular construction growth: Factory-built components and on-site assembly efficiency: Quality control advantages in controlled manufacturing environments reducing defects 60-80%. Transportation logistics requiring specialized equipment and route planning. Site preparation and crane access critical for efficient assembly scheduling.",
            "Building material transparency: Supply chain tracking and sustainability documentation: LEED and green building certification requiring detailed material sourcing documentation. Blockchain technology enabling supply chain verification from raw materials to installation. Customer demand for locally-sourced materials affecting supplier relationships and pricing structures.",
            "Drone surveys and inspections: FAA regulations and insurance requirements for contractors: Part 107 pilot certification required for commercial drone operations. Photogrammetry and LiDAR technology reducing survey costs 30-50% while improving accuracy. Insurance coverage gaps for drone operations requiring specialized policies and liability considerations.",
            "Climate resilience building: Hurricane, wildfire, and flood-resistant construction methods: Building codes evolving to address climate change impacts with stricter wind resistance and fire-resistant material requirements. Insurance premium reductions 10-25% for resilient construction methods. Material costs 15-30% higher but offset by reduced maintenance and insurance savings over building lifecycle.",
            "Skilled labor development: High school vocational programs and industry partnerships: Dual enrollment programs combining classroom education with paid apprenticeships. Industry partnerships providing equipment and instructor training to educational institutions. Career pathway clarity from entry-level to master craftsman reducing workforce turnover.",
            "Digital building permits: E-permitting systems and virtual inspection processes: Online permit applications reducing approval times 30-40% in participating jurisdictions. Virtual inspections using video conferencing and photo documentation maintaining compliance while reducing scheduling delays. Digital document management improving project coordination and reducing administrative overhead.",
        ],
        "smallbusiness": [
            "Social media marketing: TikTok and Instagram strategies for trade businesses: Before/after project videos generating 10x engagement compared to static photos. Customer testimonial videos building trust and credibility. Hashtag strategies and local SEO integration driving 25-40% increase in qualified leads for participating contractors.",
            "Remote team management: Coordinating field crews with office staff effectively: Cloud-based project management platforms enabling real-time communication between field and office. Digital time tracking and photo documentation streamlining payroll and project billing. Video conferencing for daily coordination meetings reducing travel time and improving team communication.",
            "Equipment telematics: GPS tracking and maintenance scheduling for fleet management: Vehicle tracking reducing fuel costs 10-15% through route optimization and idle time monitoring. Automated maintenance scheduling preventing costly breakdowns and extending equipment life. Theft recovery and insurance premium reductions offsetting system costs within 12-18 months.",
            "Customer relationship management: CRM systems designed specifically for contractors: Lead tracking from initial contact through project completion and warranty follow-up. Automated email sequences for project updates and maintenance reminders. Integration with accounting systems eliminating duplicate data entry and improving cash flow visibility.",
            "Succession planning: Preparing family businesses for next generation leadership: Tax implications of business transfers requiring early planning with accounting and legal professionals. Leadership development programs for next-generation family members. Employee stock ownership plans (ESOPs) as alternatives to family succession maintaining company culture while rewarding long-term employees.",
            "Cybersecurity basics: Protecting customer data and business systems from threats: Ransomware attacks targeting small businesses increasing 300% annually. Basic security measures including password management, backup systems, and employee training preventing 90% of common attacks. Cyber insurance policies becoming essential for customer contract requirements.",
            "Networking strategies: Industry associations and local business group participation: Trade association membership providing continuing education, certification programs, and peer networking opportunities. Local business referral groups generating 20-30% of new business for active participants. Chamber of Commerce involvement building community relationships and commercial project opportunities.",
        ],
    }

    normalized_subreddit = subreddit.lower()
    print(f"Normalized subreddit: {normalized_subreddit}")
    if subreddit in mock_titles:
        available_titles = mock_titles[normalized_subreddit]

        num_to_return = min(10, len(available_titles))
        selected_titles = random.sample(available_titles, num_to_return)
        return {subreddit: selected_titles}

    else:
        return {
            subreddit: f"Sorry, I don't have information on the subreddit '{subreddit}'. Please check the subreddit name."
        }


def get_reddit_contractor_news(subreddit: str) -> dict[str, list[str]]:
    """
    Fetches the top post titles from a given subreddit related to contractor and HVAC news.

    Args:
        subreddit: The name of the subreddit to fetch news from (e.g., 'hvac', 'contractors').

    Returns:
        A dictionary with the subreddit name as key and a list of
        post titles as value. Returns a message if the subreddit is unknown.
    """

    print(f"--- Tool called: Fetching from r/{subreddit} ---")

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    print(
        f"Reddit API credentials: client_id={client_id}, client_secret={client_secret}, user_agent={user_agent}"
    )

    if not client_id or not client_secret or not user_agent:
        return {
            subreddit: "Error: Reddit API credentials are not set. Please check your environment variables."
        }

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

        reddit.subreddits.search_by_name(subreddit, exact=True)
        sub = reddit.subreddit(subreddit)
        top_posts = list(sub.hot(limit=5))  # Fetch hot posts
        titles = [post.title for post in top_posts]
        if not titles:
            return {subreddit: [f"No recent hot posts found in r/{subreddit}."]}
        return {subreddit: titles}
    except PRAWException as e:
        print(f"--- Tool error: Reddit API error for r/{subreddit}: {e} ---")
        # More specific error handling could be added here (e.g., 404 for invalid sub)
        return {
            subreddit: [
                f"Error accessing r/{subreddit}. It might be private, banned, or non-existent. Details: {e}"
            ]
        }

    except Exception as e:
        return {subreddit: f"Error: Unable to connect to Reddit API. {str(e)}"}


agent = Agent(
    name="reddit_scout_agent",
    description="A Reddit Agent taht searches for the most relevant posts in a given subreddit.",
    model="gemini-1.5-flash-latest",
    instruction=(
        "You are the HVAC Contractor Scout. Your primary task is to fetch and summarize contractor and HVAC industry news."
        "1. **Identify Intent:** Determine if the user is looking for contractor news or related topics."
        "2. **Determine Subreddit:** Identify which subreddit(s) to check. Use 'hvac' by default if none are specified. Use the specific subreddit(s) if mentioned (e.g., 'r/HVAC', 'r/contractors', 'r/HomeImprovement')."
        "3. **Summarize Output:** Take the top 5-10 hot posts with their titles returned from the bot."
        "4. **Format Response:** Present the information as a concise, bulleted list. Clearly state which subreddit(s) the information came from. If the tool indicates an error or an unknown subreddit, report that error message."
        "5. **MUST CALL TOOL:** You **MUST** call the `get_mock_reddit_contractor_news` tool with the identified subreddit(s). Do NOT generate summaries without calling the tool first."
    ),
    tools=[get_reddit_contractor_news],
)
