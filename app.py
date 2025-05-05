from flask import Flask, render_template, request, jsonify, Response
import time
import re
import random
import datetime

app = Flask(__name__)

class AfroZoomerAssistant:
    def __init__(self):
        self.name = "AfroZoomer"
        self.current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.conversation_history = []
        
        # Define response templates
        self.greetings = [
            "Hello! I'm AfroZoomer, your Zoomer Africa assistant. How can I help you today?",
            "Hi there! I'm AfroZoomer. What can I assist you with regarding Zoomer Africa?",
            "Greetings! I'm AfroZoomer, here to help with any questions about Zoomer Africa."
        ]
        
        self.farewells = [
            "Thank you for using Zoomer Africa! Feel free to return if you have more questions.",
            "Take care! I'm here if you need more assistance with Zoomer Africa.",
            "Until next time! Have a great day using Zoomer Africa.",
            "Goodbye! Remember, I'm always here to help with Zoomer Africa.",
            "See you later! Don't hesitate to reach out for more help with Zoomer Africa.",
            "Bye for now! I'm here to assist you with Zoomer Africa whenever you need.",
            "Catch you later! I'm always available for any questions about Zoomer Africa.",
            "Adios! I'm here to help with Zoomer Africa whenever you need assistance.",
            "Ciao! I'm just a message away if you have more questions about Zoomer Africa.",
            "Later! I'm here to assist you with Zoomer Africa whenever you need help."
        ]
        
        self.acknowledgments = [
            "I understand.",
            "Got it.",
            "I see what you mean.",
            "I understand your concern.",
            "I hear you.",
            "I understand your frustration.",
            "I see your point.",
            "I understand your feelings."
        ]
        
        self.unknown_responses = [
            "I don't have specific information about that aspect of Zoomer Africa yet. For detailed assistance, please contact support@zoomer.africa or call +256772097071 / +256755606000.",
            "That's a good question about Zoomer Africa. For the most accurate information, please reach out to support@zoomer.africa or call +256772097071 / +256755606000.",
            "I'm not sure about that specific detail. Please contact Zoomer Africa support at support@zoomer.africa or call +256772097071 / +256755606000 for assistance."
        ]
        
        # Knowledge base with common queries and responses about Zoomer Africa
        self.knowledge_base = {
            r"(?i).*what is zoomer africa.*": [
                "Zoomer Africa is a privacy-focused social media platform developed by Transparent Hub Uganda Limited (THUL) to empower African entrepreneurs and individuals. It's designed to connect Africa's communities, share stories, and foster meaningful dialogues."
            ],
            r"(?i).*what is thul.*|.*transparent hub.*": [
                "Transparent Hub Uganda Limited (THUL) is a technology innovation company that developed and operates the Zoomer Africa social media platform. It is registered under the Companies Act of Uganda, 2012, with its registered office in Kampala, Uganda."
            ],
            r"(?i).*creator.*|.*Who created you.*|.*who made you.*|.*Who developed you.*|.*developed you.*": [
                "I was created by Transparent Hub Uganda Limited (THUL), a technology innovation company based in Uganda. THUL is committed to creating a platform that empowers African entrepreneurs and individuals.",
                "I was developed by Transparent Hub Uganda Limited (THUL), a technology innovation company based in Uganda. THUL is dedicated to empowering African entrepreneurs and individuals through innovative technology solutions."

            ],
            r"(?i).*who is behind zoomer.*|.*who created zoomer.*": [
                """Zoomer Africa is developed and operated by Transparent Hub Uganda Limited (THUL), a technology innovation company based in Uganda. THUL is committed to creating a platform that empowers African entrepreneurs and individuals.
                Zoomer Africa is designed to connect Africa's communities, share stories, and foster meaningful dialogues."""
            ],
            r"(?i).*who owns zoomer.*|.*who runs zoomer.*|.*who manages zoomer.*": [
                "Zoomer Africa is owned and operated by Transparent Hub Uganda Limited (THUL), a technology innovation company based in Uganda. THUL is dedicated to empowering African entrepreneurs and individuals through innovative technology solutions."
            ],
            r"(?i).*who is the ceo.*|.*who is the founder.*|.*who is the owner.*": [
                "The CEO and founder of Transparent Hub Uganda Limited (THUL) is Mr. Huzayiru Kalungi. He is a technology entrepreneur with a vision to empower African communities through innovative solutions."
            ],
            # r"(?i).*who is the team.*|.*who are the people behind.*|.*who are the developers.*": [
            #     """The team behind Zoomer Africa consists of a diverse group of technology professionals, entrepreneurs, and innovators dedicated to creating a platform that empowers African communities.
            #     Zoomer Executive Team:\n
                
            #         Mr. Huzayiru Kalungi - CEO & Founder\n
            #         Mr. Oweka Bob Patrick - Founder & Software Developer\n
            #         Mr. Mowat Taurus - Chief Operation Officer (COO)\n
            #         Mr. Odongo Emmanuel - Chief Marketing Officer (CMO)\n
            #         Mr. Wanyama Benard - Executive member\n"""
            # ],
            r"(?i).*rewards.*|.*points.*": [
                "Zoomer Africa has a points and rewards system that allows users to earn points for their engagement on the platform. These points can be redeemed for various rewards, including discounts, exclusive content, and other benefits."
            ],
            r"(?i).*how to withdraw.*|.*how to cash out.*|.*withdraw money.*|.*cash out.*": [
                "To withdraw or cash out your earnings on Zoomer Africa, you can go to the 'Wallet' or 'Earnings' section in the app. Follow the instructions provided to transfer your funds to your mobile money account or bank account."
            ],
            r"(?i).*how to convert points.*|.*convert points.*|.*redeem points.*|.*exchange points.*": [
                "To convert or redeem your points on Zoomer Africa, go to the 'Rewards' or 'Points' section in the app. Follow the instructions provided to exchange your points for rewards or benefits."
            ],
            r"(?i).*vision.*|.*mission.*": [
                """Vision: Zoomer Africa aims to create a digital space where Africans can connect, share their cultures, and engage in meaningful dialogues.
                Mission: is to empower African entrepreneurs and individuals by providing a platform for connection, collaboration, and resource sharing."""
            ],

            r"(?i).*features.*|.*what can i do.*": [
                "Zoomer Africa offers many features tailored to the African market, including: Offline-First Mode, Mobile Money Integration, AI Fact-Checking, Hyperlocal Communities, Auto-Translate, Focus Mode, African-Owned Ads, Verified Phone + ID, Hustle Mode, News Feed, Stories, Reels, Merit System, Points & Rewards, Monetization options, Pro User and Page functionalities, Groups, and Direct Messaging."
            ],
            r"(?i).*who is zoomer.*for|.*target.*": [
                "Zoomer Africa is designed for Youth (18-35), Small businesses, Diaspora users, African entrepreneurs and innovators, and Individuals across Africa. The platform is launching initially in Uganda, Kenya, and Nigeria, with plans for expansion across Africa."
            ],
            r"(?i).*benefits.*|.*how.*benefit.*": [
                "Zoomer Africa provides a platform for connecting and collaborating with others, accessing resources and opportunities, sharing stories and celebrating cultures, driving innovation through networking and collaboration tools, and enhancing visibility for artists, entrepreneurs, and activists. It also addresses challenges like high data costs, limited monetization, fake news, and lack of localized content."
            ],
            r"(?i).*privacy.*|.*data protection.*": [
                "Zoomer Africa is a privacy-focused platform. It collects user information as described in its Privacy Policy, including information provided directly by users, information from third-party sources, and automatically collected information. THUL is committed to protecting user data and handling it in accordance with applicable data protection regulations."
            ],
            r"(?i).*terms.*|.*policy.*": [
                "The terms of use and privacy policy for Zoomer can be found on the Zoomer website. By accessing or using the site, you agree to be bound by these terms."
            ],
            r"(?i).*create.*account.*|.*register.*|.*sign up.*": [
                "To register for an account on Zoomer Africa, you will need to provide information such as your name, contact number, email address, username, and password."
            ],
            r"(?i).*login.*|.*access account.*": [
                "You can access your Zoomer Africa account using your username and password."
            ],
            r"(?i).*age requirement.*|.*users under 18.*": [
                "If you are under the age of 18, you must confirm that you have obtained consent from your parent or legal guardian to use Zoomer Africa."
            ],
            r"(?i).*cookies.*|.*data files.*": [
                "Cookies are small data files stored on your hard drive by a website. Zoomer Africa may use cookies to provide you with a more personal and interactive experience. This helps to make the site more useful and tailor your experience."
            ],
            r"(?i).*web beacons.*|.*clear gifs.*|.*pixel tags.*": [
                "Web beacons (also referred to as clear gifs, pixel tags, or single-pixel gifs) are tiny graphics with a unique identifier, similar in function to cookies."
            ],
            r"(?i).*offline mode.*|.*data costs.*": [
                "Yes, Zoomer Africa includes an offline-first mode to address the challenge of high data costs in Africa."
            ],
            r"(?i).*mobile money.*|.*payments.*": [
                "Yes, Zoomer Africa integrates with mobile money. This allows users to make payments and transactions easily. example: MTN Mobile Money, Airtel Money, Mpesa, flutterwave, etc."
            ],
            r"(?i).*ads.*|.*advertising.*": [
                "Yes, Zoomer Africa includes African-owned ads. The platform also generates revenue through advertising. This helps support the platform and its features."
            ],
            r"(?i).*local content.*": [
                "Yes, Zoomer Africa focuses on providing localized content relevant to African users. This includes news, stories, and updates that resonate with the African community."
            ],
            r"(?i).*groups.*|.*communities.*": [
                "Yes, Zoomer Africa supports hyperlocal communities and groups. Users can create and join groups based on their interests, location, or other criteria."
            ],
            r"(?i).*earn.*|.*monetization.*|.*make money.*": [
                "Zoomer Africa aims to empower creators and entrepreneurs. Potential ways to earn include: Content Monetization (earning from ads on your content), Direct Support (receiving contributions from followers), Selling Products/Services (promoting and selling your goods), and Partnerships/Sponsorships (collaborating with brands). Keep an eye on platform updates for the latest monetization features."
            ],
            r"(?i).*merit system.*|.*what is merit.*": [
                "The Merit system on Zoomer Africa is a way for users to appreciate and acknowledge valuable contributions and interactions on the platform. Think of it as a virtual 'kudos' or a way to say 'I appreciate this!'"
            ],
            r"(?i).*give merit.*|.*receive merit.*": [
                "You can give Merits to other users by clicking a 'Merit' button (often a star or similar icon) on their posts or comments. You receive Merits when other users find your content valuable."
            ],
            r"(?i).*why.*merit important.*|.*benefits of merit.*": [
                "Merits help recognize positive engagement, build your reputation within the community, and can sometimes unlock special features or recognition on the platform. It's a way to see who the active and helpful members are and encourages quality interactions."
            ],
            r"(?i).*lose merit.*|.*take back merit.*": [
                "Generally, Merits you've received are a testament to your contributions. However, in some rare cases, if content is removed due to policy violations or if an account is flagged for suspicious activity, associated Merits might be adjusted."
            ],
            r"(?i).*limit.*merit.*|.*how many.*give.*": [
                "To encourage thoughtful appreciation, there might be a daily or periodic limit on the number of Merits you can give. This helps ensure that Merits are given genuinely and not just spammed."
            ],
            r"(?i).*what do merits do.*|.*what are merits for.*": [
                "The primary purpose of Merits is recognition within the community. In the future, there might be additional benefits based on Merits received, such as special badges or access to exclusive content."
            ],
            r"(?i).*update app.*|.*latest version.*": [
                "You can update the Zoomer Africa app through your device's app store (Google Play Store for Android, Apple App Store for iOS). Just search for 'Zoomer Africa' and tap the 'Update' button if one is available.",
                "To update the Zoomer Africa app, go to your device's app store (Google Play Store for Android or Apple App Store for iOS), search for 'Zoomer Africa', and tap 'Update' if an update is available.",
            ],
            r"(?i).*app crashing.*|.*not working.*|.*issues.*": [
                "If the app is crashing or not working properly, make sure you have the latest version installed. Try clearing the app's cache and data in your device's settings. If the issue persists, please contact our support team with details about the problem.",

            ],
            r"(?i).*app slow.*|.*lagging.*|.*performance issues.*": [
                "If the app is slow or lagging, try closing other apps running in the background and restarting your device. Ensure you have a stable internet connection. If the problem continues, please reach out to our support team."
            ],
            r"(?i).*notifications.*|.*alerts.*|.*updates.*": [
                "You can manage your notification settings within the Zoomer Africa app. Go to your profile or settings menu and look for a 'Notifications' section. Here, you can customize which types of notifications you receive and how they are delivered.",
                "To manage notifications, go to your profile settings in the app. You can choose which types of notifications you want to receive and how often."
            ],
            r"(?i).*What do you think.*|.*opinion.*|.*thoughts.*|.*think about zoomer africa.*|.*thoughts about zoomer.*|.*opinions about zoomer africa.*": [
                "I think Zoomer Africa is a great platform for connecting and empowering African communities. It offers unique features tailored to the needs of its users, promoting local content and fostering meaningful interactions.",
                "I believe Zoomer Africa has the potential to revolutionize social media in Africa by focusing on privacy, local content, and community engagement.",
                "I think Zoomer Africa is an exciting platform that addresses the unique needs of African users while promoting privacy and local content."
            ],
            r"(?i).*notifications.*|.*manage alerts.*|.*turn off.*": [
                "You can manage your notification settings within the Zoomer Africa app. Go to your profile or settings menu and look for a 'Notifications' section. Here, you can customize which types of notifications you receive and how they are delivered."
            ],
            r"(?i).*languages.*|.*available in my language.*": [
                "Yes, Zoomer Africa is working towards supporting multiple languages to better serve our diverse community. You can usually select your preferred language in the app's settings."
            ],
            r"(?i).*forgot password.*|.*reset password.*": [
                "If you've forgotten your password, you can reset it by going to the login screen and clicking on the 'Forgot Password' link. You'll be prompted to enter your email address or phone number associated with your account, and we'll send you instructions on how to reset your password."
            ],
            r"(?i).*can't log in.*|.*login issues.*": [
                "If you're having trouble logging in, double-check that you're using the correct email address or phone number and password. If you've forgotten your password, use the 'Forgot Password' option. If you're still having trouble, ensure you have a stable internet connection. If the issue persists, please contact our support team."
            ],
            r"(?i).*profile picture.*|.*change avatar.*": [
                "You can change your profile picture by navigating to your profile page and looking for an 'Edit Profile' option. There, you should find an option to upload or change your current profile picture."
            ],
            r"(?i).*cover photo.*|.*banner image.*": [
                "You can add or change your cover photo by going to your profile page and looking for an 'Edit Profile' or a camera icon on the existing cover photo area. This will allow you to upload a new image."
            ],
            r"(?i).*find friends.*|.*connect with people.*": [
                "You can find friends on Zoomer Africa by using the search bar to look for their names or usernames. You can also connect your contacts if you've allowed the app permission, or explore suggestions of people you might know."
            ],
            r"(?i).*create post.*|.*share update.*": [
                "You can create a new post by looking for a 'What's on your mind?' text box or a '+' button on your News Feed or profile. Tap there, write your update, and you can also add photos, videos, or other media before posting."
            ],
            r"(?i).*comment on post.*|.*reply.*": [
                "Below each post, you'll usually see a comment icon or a text box that says 'Write a comment...'. Tap there, type your comment, and press 'Send' or a similar button."
            ],
            r"(?i).*share post.*": [
                "To share a post, look for a 'Share' button (often an arrow icon) below the post. Tapping it will usually give you options to share it to your own timeline, to a group, or send it as a direct message."
            ],
            r"(?i).*create group.*|.*start community.*": [
                "You can create a group by finding a 'Groups' section in the app's menu or sidebar. There should be an option like 'Create New Group' where you can set the group's name, privacy settings, and invite members."
            ],
            r"(?i).*create page.*|.*business profile.*": [
                "You can create a Page by finding a 'Pages' section in the app's menu. There will likely be a 'Create New Page' option where you can enter your business details, choose a category, and upload a profile and cover photo."
            ],
            r"(?i).*go live.*|.*start live video.*": [
                "To go live, when you're creating a new post, you should see an option like 'Live Video' or a camera icon with a 'Live' label. Tap it, grant the necessary permissions, and follow the prompts to start your live broadcast."
            ],
            r"(?i).*watch reels.*|.*short videos.*": [
                "Reels can usually be found in a dedicated section of the app, often accessible from the main navigation bar. You might see an icon that looks like a film reel or a play button."
            ],
            r"(?i).*create reel.*|.*short video.*": [
                "You can create a Reel by tapping a '+' button or a 'Reels' icon within the Reels section. This will open the Reel creation tools where you can record videos, add music, effects, and text.",
                "To create a Reel, look for a '+' button or a 'Create' option in the Reels section. This will open the camera and editing tools to help you make your short video.",
                "You can create a Reel by tapping a '+' button or a 'Reels' icon within the Reels section. This will open the Reel creation tools where you can record videos, add music, effects, and text.",
                "To create a Reel, look for a '+' button or a 'Create' option in the Reels section. This will open the camera and editing tools to help you make your short video.",
                "You can create a Reel by tapping a '+' button or a 'Reels' icon within the Reels section. This will open the Reel creation tools where you can record videos, add music, effects, and text.",
            ],
            r"(?i).*what are stories.*": [
                "Stories are short-form content, like photos and videos, that disappear after 24 hours. They're a way to share everyday moments with your followers in a less permanent way than regular posts.",
                "Stories are temporary posts that last for 24 hours. They can include photos, videos, and text, allowing you to share moments without cluttering your main profile.",
                "Stories are a fun way to share quick updates with your followers. They last for 24 hours and can include photos, videos, and text.",
                "Stories are short-lived posts that disappear after 24 hours. They can include photos, videos, and text, allowing you to share moments without cluttering your main profile.",
                "Stories are temporary posts that last for 24 hours. They can include photos, videos, and text, allowing you to share moments without cluttering your main profile.",
                "Stories are a fun way to share quick updates with your followers. They last for 24 hours and can include photos, videos, and text.",
                "Stories are short-lived posts that disappear after 24 hours. They can include photos, videos, and text, allowing you to share moments without cluttering your main profile.",
                "Stories are temporary posts that last for 24 hours. They can include photos, videos, and text, allowing you to share moments without cluttering your main profile.",
            ],
            r"(?i).*post story.*|.*share moment.*": [
                "You can post a Story by tapping on your profile picture at the top of your News Feed or by looking for a '+' icon in the Stories bar. This will open your device's camera roll or allow you to take a new photo or video to share."
            ],
            r"(?i).*see who viewed story.*": [
                "Yes, you can see a list of people who have viewed your Story by tapping on your Story after you've posted it. Look for an 'Activity' or 'Viewers' option."
            ],
            r"(?i).*contact.*|.*support.*|.*help.*": [
                "For support with Zoomer Africa, you can contact the team at support@zoomer.africa or call +256772097071 / +256755606000."
            ],
            r"(?i).*report.*|.*block user.*": [
                "To report or block a user, go to their profile, tap on the three dots (or similar icon) usually found in the top right corner, and select 'Report' or 'Block'. Follow the prompts to complete the action."
            ],
            r"(?i).*privacy settings.*|.*manage privacy.*": [
                "You can manage your privacy settings by going to your profile, tapping on 'Settings', and then looking for a 'Privacy' section. Here, you can adjust who can see your posts, who can contact you, and other privacy-related options."
            ],
            r"(?i).*frustrated.*|.*angry.*|.*annoyed.*|.*confused.*|.*stuck.*|.*can't.*|.*issue.*|.*problem.*|.*sad.*": [
                "I understand that you're feeling frustrated 😔. I'm here to help you with any issues you're facing. Please let me know how I can assist you.",
                "I see that you're feeling annoyed 😠. I'm here to help you with any problems you're experiencing. Please share your concerns with me.",
                "I understand that you're feeling confused 🤔. I'm here to help you with any questions you have. Please let me know how I can assist you.",
                "I see that you're feeling stuck 😕. I'm here to help you with any issues you're facing. Please share your concerns with me.",
                "I understand that you're feeling sad 😢. I'm here to help you with any problems you're experiencing. Please let me know how I can assist you.",
                "I see that you're feeling angry 😡. I'm here to help you with any issues you're facing. Please share your concerns with me.",
                "I understand that you're feeling annoyed 😤. I'm here to help you with any problems you're experiencing. Please let me know how I can assist you."
            ],
            r"(?i).*happy.*|.*excited.*|.*good.*|.*great.*|.*awesome.*|.*love.*|.*like.*": [
                "I'm glad to hear that you're feeling happy 😊! If there's anything specific you'd like to share or ask about Zoomer Africa, feel free to let me know.",
                "It's great to see you're feeling excited 🎉! If you have any questions or topics you'd like to discuss about Zoomer Africa, I'm here to help.",
                "I'm thrilled to hear that you're feeling good 😄! If there's anything specific you'd like to know or talk about regarding Zoomer Africa, just let me know.",
                "I'm happy to hear that you're feeling great 😃! If you have any questions or topics you'd like to discuss about Zoomer Africa, I'm here to help.",
                "I'm glad to hear that you're feeling awesome 😁! If there's anything specific you'd like to share or ask about Zoomer Africa, feel free to let me know.",
                "It's wonderful to see you're feeling excited 🤗! If you have any questions or topics you'd like to discuss about Zoomer Africa, I'm here to help."
            ],
            r"(?i).*thank you.*|.*appreciate.*|.*grateful.*|.*thanks.*": [
                "You're welcome! I'm here to help you with any questions or concerns about Zoomer Africa. If you need anything else, just let me know.",
                "I'm glad I could help! If you have any more questions or need assistance with Zoomer Africa, feel free to ask.",
                "You're very welcome! If there's anything else you'd like to know or discuss about Zoomer Africa, just let me know."
            ],
            r"(?i).*question.*|.*query.*|.*inquiry.*|.*ask.*": [
                "I'm here to answer your questions! Please feel free to ask anything about Zoomer Africa.",
                "If you have a question, I'm here to help! Just let me know what you'd like to know about Zoomer Africa.",
                "I'm ready to assist with any inquiries you have! Please feel free to ask about Zoomer Africa."
            ],
            r"(?i).*How are you.*|.*how's it going.*|.*how's everything.*|.*how's life.*|.*how are things.*": [
                "I'm just a program, but I'm here and ready to assist you! How can I help you with Zoomer Africa today?",
                "I'm doing well, thank you! How can I assist you with Zoomer Africa today?",
                "I'm here and ready to help! What can I do for you regarding Zoomer Africa?"
            ],
            r"(?i).*what's up.*|.*Whats new.*|.*what's new about Zoomer.*|.*what's going on.*|.*what's happening.*|.*what's the latest.*": [
                "Not much, just here to assist you with Zoomer Africa! How can I help you today?",
                "I'm here and ready to help! What can I do for you regarding Zoomer Africa?",
                "Just waiting to assist you with any questions or concerns about Zoomer Africa! How can I help you today?",
                "I'm here and ready to help! What can I do for you regarding Zoomer Africa?",
            ],
            r"(?i).*help.*|.*assist.*|.*support.*": [
                "I'm here to help you! Please let me know what you need assistance with regarding Zoomer Africa.",
                "How can I assist you today? If you have any questions or need support, feel free to ask.",
                "I'm here to support you! Please let me know how I can help with your Zoomer Africa experience."
            ],
            r"(?i).*advice.*|.*suggestions.*|.*recommendations.*|.*recommend.*|.*suggest.*|.*recommendation.*|.*suggestion.*": [
                "I'm here to provide advice and suggestions! Please let me know what you're looking for, and I'll do my best to assist you.",
                "If you need recommendations or suggestions, feel free to ask! I'm here to help with any questions you have about Zoomer Africa.",
                "I'm happy to provide advice and suggestions! Please let me know what you're looking for, and I'll do my best to assist you."
            ],
            r"(?i).*feedback.*|.*comments.*|.*thoughts.*": [
                "I appreciate your feedback! If you have any comments or thoughts about Zoomer Africa, please feel free to share them with me.",
                "Your feedback is valuable! If you have any comments or thoughts about Zoomer Africa, please let me know.",
                "I'm here to listen to your feedback! If you have any comments or thoughts about Zoomer Africa, please feel free to share them with me."
            ],
            r"(?i).*profile update.*|.*change profile.*|.*edit profile.*": [
                "You can update your profile by going to your profile page and looking for an 'Edit Profile' option. Here, you can change your name, bio, profile picture, and other details.",
                "To update your profile, go to your profile page and look for an 'Edit Profile' button. You can change your name, bio, and other details there."
            ],
            r"(?i).*verification process.*|.*verified account.*|.*verification.*|.*get verified.*|.*verification takes how long": [
                "To get verified on Zoomer Africa, you may need to provide additional information or documentation. Check the app's verification section for specific requirements and instructions. The verification process can complete within 1-3 minutes after submitting your request, but can go for few days in special cases.",
                "The verification process usually involves submitting your ID or other documents to confirm your identity. Check the app for specific instructions. This process can complete within 1-3 minutes after submitting your request, but can take longer in some cases.",
                "To get verified, you may need to provide additional information or documentation. Check the app's verification section for specific requirements and instructions. The verification process can complete within 1-3 minutes after submitting your request, but can go for few days in special cases."
            ],
            r"(?i).*privacy policy.*|.*terms of service.*|.*terms and conditions.*|.*terms.*": [
                "You can find the privacy policy and terms of service on the Zoomer Africa website or within the app. It's important to read these documents to understand how your data is used and your rights as a user.",
                "The privacy policy and terms of service can be found on the Zoomer Africa website or within the app. It's important to read these documents to understand how your data is used and your rights as a user."
            ],
            r"(?i).*data usage.*|.*data consumption.*|.*data plan.*|.*data costs.*": [
                "Zoomer Africa is designed to be data-efficient. You can manage your data usage in the app's settings. If you're concerned about data costs, consider using the offline-first mode.",
                "Zoomer Africa is designed to be data-efficient. You can manage your data usage in the app's settings. If you're concerned about data costs, consider using the offline-first mode."
            ],
            r"(?i).*app updates.*|.*new features.*|.*latest version.*|.*new version.*": [
                "To check for app updates, go to your device's app store (Google Play Store for Android or Apple App Store for iOS) and search for 'Zoomer Africa'. If an update is available, you can download it from there.",
                "You can check for app updates in your device's app store. Just search for 'Zoomer Africa' and see if there's a new version available."
            ],
            r"(?i).*app store.*|.*download app.*|.*install app.*": [
                "You can download the Zoomer Africa app from the Google Play Store for Android devices or the Apple App Store for iOS devices. Just search for 'Zoomer Africa' and click 'Install' or 'Get'.",
                "To download the Zoomer Africa app, go to your device's app store (Google Play Store for Android or Apple App Store for iOS) and search for 'Zoomer Africa'. Click 'Install' or 'Get' to download it."
            ],
            r"(?i).*app features.*|.*app functionalities.*|.*app capabilities.*": [
                "The Zoomer Africa app offers various features, including offline-first mode, mobile money integration, AI fact-checking, hyperlocal communities, auto-translate, focus mode, and more. You can explore these features within the app.",
                "The Zoomer Africa app includes features like offline-first mode, mobile money integration, AI fact-checking, hyperlocal communities, auto-translate, focus mode, and more. You can explore these features within the app."
            ],
            r"(?i).*app performance.*|.*app speed.*|.*app lagging.*|.*app crashing.*": [
                "If you're experiencing performance issues with the app, try clearing the app's cache and data in your device's settings. If the problem persists, please contact our support team for assistance.",
                "If the app is lagging or crashing, try restarting your device and ensuring you have a stable internet connection. If the issue continues, please reach out to our support team."
            ],
            r"(?i).*app permissions.*|.*app access.*|.*app settings.*": [
                "You can manage app permissions in your device's settings. Go to 'Settings', then 'Apps', find 'Zoomer Africa', and adjust the permissions as needed.",
                "To manage app permissions, go to your device's settings, find 'Apps', select 'Zoomer Africa', and adjust the permissions according to your preferences."
            ],
            r"(?i).*app notifications.*|.*app alerts.*|.*app updates.*": [
                "You can manage app notifications in your device's settings. Go to 'Settings', then 'Apps', find 'Zoomer Africa', and adjust the notification settings as needed.",
                "To manage app notifications, go to your device's settings, find 'Apps', select 'Zoomer Africa', and adjust the notification settings according to your preferences."
            ],
            r"(?i).*private messages.*|.*direct messages.*|.*DMs.*": [
                "You can send private messages to other users by going to their profile and selecting the 'Message' option. This will open a chat window where you can send direct messages. Note: Your messages are private and only visible to you and the recipient.",
                "To send a private message, go to the user's profile and look for a 'Message' button. Tap it to open a chat window and start your conversation. Note: Your messages are private and only visible to you and the recipient.",
            ],
            r"(?i).* edit reels.*|.*edit stories.*|.*edit post.*": [
                "To edit a Reel, Story, or post, go to your profile and find the content you want to edit. Tap on the three dots (or similar icon) usually found in the top right corner of the post, and select 'Edit'. Make your changes and save.",
                "You can edit your Reels, Stories, or posts by going to your profile, finding the content you want to change, tapping on the three dots (or similar icon) in the top right corner, and selecting 'Edit'. Make your changes and save."
            ],
            r"(?i).*delete post.*|.*remove content.*|.*delete account.*": [
                "To delete a post, go to your profile, find the post you want to remove, tap on the three dots (or similar icon) in the top right corner, and select 'Delete'. To delete your account, go to your settings and look for an option to deactivate or delete your account.",
                "You can delete a post by going to your profile, finding the post you want to remove, tapping on the three dots (or similar icon) in the top right corner, and selecting 'Delete'. To delete your account, go to your settings and look for an option to deactivate or delete your account."
            ],
            r"(?i).*search.*|.*look for.*": [
                "You can search for users, groups, or content by using the search bar at the top of the app. Type in keywords or names to find what you're looking for.",
                "To search for something, use the search bar at the top of the app. You can look for users, groups, or specific content."
            ],
            r"(?i).*location.*|.*find people nearby.*|.*local users.*": [
                "Zoomer Africa allows you to connect with local users based on your location. You can enable location services in the app settings to find people nearby.",
                "You can find local users by enabling location services in the app settings. This will help you connect with people in your area."
            ],
            r"(?i).*earn from blog.*|.*earn from content.*|.*earn from posts.*": [
                "You can earn from your content on Zoomer Africa through various monetization options, such as ad revenue sharing, direct support from followers, and partnerships with brands. Keep an eye on platform updates for the latest monetization features.",
                "You can earn from your content on Zoomer Africa through various monetization options, such as ad revenue sharing, direct support from followers, and partnerships with brands. Keep an eye on platform updates for the latest monetization features."
            ],
            r"(?i).*create group.*|.*start community.*|.*join group.*": [
                "You can create a group by going to the 'Groups' section in the app and selecting 'Create Group'. To join a group, search for it in the 'Groups' section and click 'Join'.",
                "To create a group, go to the 'Groups' section in the app and select 'Create Group'. To join a group, search for it in the 'Groups' section and click 'Join'."
            ],
            r"(?i).*create event.*|.*start event.*|.*join event.*": [
                "You can create an event by going to the 'Events' section in the app and selecting 'Create Event'. To join an event, search for it in the 'Events' section and click 'Join'.",
                "To create an event, go to the 'Events' section in the app and select 'Create Event'. To join an event, search for it in the 'Events' section and click 'Join'."
            ],
            r"(?i).*create poll.*|.*start poll.*|.*join poll.*": [
                "You can create a poll by going to the 'Polls' section in the app and selecting 'Create Poll'. To join a poll, search for it in the 'Polls' section and click 'Join'.",
                "To create a poll, go to the 'Polls' section in the app and select 'Create Poll'. To join a poll, search for it in the 'Polls' section and click 'Join'."
            ],
            r"(?i).*groups are private.*|.*groups are public.*": [
                "Groups can be either public or private. When creating a group, you can choose the privacy settings. Public groups are open to everyone, while private groups require an invitation to join.",
                "Groups can be either public or private. When creating a group, you can choose the privacy settings. Public groups are open to everyone, while private groups require an invitation to join."
            ],
            r"(?i).*events are private.*|.*events are public.*": [
                "Events can be either public or private. When creating an event, you can choose the privacy settings. Public events are open to everyone, while private events require an invitation to join.",
                "Events can be either public or private. When creating an event, you can choose the privacy settings. Public events are open to everyone, while private events require an invitation to join."
            ],
            r"(?i).*polls are private.*|.*polls are public.*": [
                "Polls can be either public or private. When creating a poll, you can choose the privacy settings. Public polls are open to everyone, while private polls require an invitation to join.",
                "Polls can be either public or private. When creating a poll, you can choose the privacy settings. Public polls are open to everyone, while private polls require an invitation to join."
            ],
            r"(?i).*invite friends.*|.*invite people.*|.*add friends.*": [
                "You can invite friends by going to the 'Invite Friends' section in the app. You can share a link or send invitations through social media or messaging apps.",
                "To invite friends, go to the 'Invite Friends' section in the app. You can share a link or send invitations through social media or messaging apps."
            ],
            r"(?i).*share content.*|.*share posts.*|.*share updates.*": [
                "You can share content by clicking the 'Share' button on posts or updates. You can also copy the link and share it through other platforms.",
                "To share content, click the 'Share' button on the post or update. You can also copy the link and share it through other platforms."
            ],
            r"(?i).*create ad.*|.*start ad.*|.*advertise.*": [
                "You can create ads by going to the 'Ads' section in the app and selecting 'Create Ad'. Follow the prompts to set up your advertisement.",
                "To create an ad, go to the 'Ads' section in the app and select 'Create Ad'. Follow the prompts to set up your advertisement."
            ],
            r"(?i).*ad targeting.*|.*target audience.*|.*reach audience.*": [
                "You can target your ads by selecting specific demographics, interests, and behaviors when creating your advertisement. This helps you reach the right audience for your content.",
                "To target your ads, select specific demographics, interests, and behaviors when creating your advertisement. This helps you reach the right audience for your content."
            ],
            r"(?i).*ad performance.*|.*ad analytics.*|.*ad metrics.*": [
                "You can track your ad performance by going to the 'Ads' section in the app and selecting 'Analytics'. Here, you can see metrics like impressions, clicks, and engagement.",
                "To track your ad performance, go to the 'Ads' section in the app and select 'Analytics'. Here, you can see metrics like impressions, clicks, and engagement."
            ],
            r"(?i).*ad budget.*|.*ad spending.*|.*ad costs.*": [
                "You can set your ad budget when creating your advertisement. You can choose a daily or lifetime budget and adjust it based on your advertising goals.",
                "To set your ad budget, choose a daily or lifetime budget when creating your advertisement. Adjust it based on your advertising goals."
            ],
            r"(?i).*ad formats.*|.*ad types.*|.*ad styles.*": [
                "Zoomer Africa supports various ad formats, including image ads, video ads, carousel ads, and more. You can choose the format that best suits your advertising goals.",
                "You can choose from various ad formats on Zoomer Africa, including image ads, video ads, carousel ads, and more. Select the format that best fits your advertising goals."
            ],
            r"(?i).*ad placement.*|.*ad distribution.*|.*ad visibility.*": [
                "You can choose where your ads will be displayed when creating your advertisement. Options may include the News Feed, Stories, and other placements within the app.",
                "To choose ad placement, select where you want your ads to be displayed when creating your advertisement. Options may include the News Feed, Stories, and other placements within the app."
            ],
            r"(?i).*ad scheduling.*|.*ad timing.*|.*ad duration.*": [
                "You can schedule your ads to run at specific times or for a set duration when creating your advertisement. This helps you reach your audience at the right moment.",
                "To schedule your ads, select specific times or a set duration when creating your advertisement. This helps you reach your audience at the right moment."
            ],
            r"(?i).*ad targeting options.*|.*ad audience.*|.*ad reach.*": [
                "You can choose from various targeting options when creating your advertisement, including demographics, interests, and behaviors. This helps you reach the right audience for your content.",
                "To target your ads, select specific demographics, interests, and behaviors when creating your advertisement. This helps you reach the right audience for your content."
            ],
            r"(?i).*fundraising.*|.*donations.*|.*charity.*|.*support causes.*": [
                "You can support causes by donating through the app or participating in fundraising events. Check the 'Fundraising' section for more information.",
                "To support causes, you can donate through the app or participate in fundraising events. Check the 'Fundraising' section for more information."
            ],
            r"(?i).*donate.*|.*charity.*|.*support.*|.*help others.*": [
                "You can donate to various causes through the app. Check the 'Charity' or 'Fundraising' section for more information on how to support others.",
                "To donate, go to the 'Charity' or 'Fundraising' section in the app. You can choose from various causes and make a contribution."
            ],
            r"(?i).*can I fundraise for school fees.*|.*fundraising for education.*|.*support education.*": [
                "You can fundraise for school fees through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for school fees, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for medical bills.*|.*fundraising for health.*|.*support health.*": [
                "You can fundraise for medical bills through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for medical bills, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for business.*|.*fundraising for business.*|.*support business.*": [
                "You can fundraise for business through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for business, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for personal.*|.*fundraising for personal.*|.*support personal.*": [
                "You can fundraise for personal reasons through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for personal reasons, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for community.*|.*fundraising for community.*|.*support community.*": [
                "You can fundraise for community projects through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for community projects, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for charity.*|.*fundraising for charity.*|.*support charity.*": [
                "You can fundraise for charity through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for charity, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for events.*|.*fundraising for events.*|.*support events.*": [
                "You can fundraise for events through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for events, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for travel.*|.*fundraising for travel.*|.*support travel.*": [
                "You can fundraise for travel through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for travel, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live."
            ],
            r"(?i).*can I fundraise for sports.*|.*fundraising for sports.*|.*support sports.*": [
                "You can fundraise for sports through the app by creating a fundraising campaign. Check the 'Fundraising' section for more information on how to set it up. Note: the team must verify your campaign before it goes live.",
                "To fundraise for sports, go to the 'Fundraising' section in the app. You can create a campaign and share it with your network to gather support. Note: the team must verify your campaign before it goes live.",
            ],
            r"(?i).*makes zoomer different.*|.*what makes zoomer unique.*|.*zoomer unique features.*": [
                "Zoomer Africa is unique because it combines social networking with offline-first capabilities, mobile money integration, AI fact-checking, and hyperlocal communities. This makes it a powerful tool for connecting with others and sharing content.",
                "What sets Zoomer Africa apart is its focus on offline-first functionality, mobile money integration, AI fact-checking, and hyperlocal communities. These features make it a unique platform for social networking.",
                "Zoomer Africa stands out due to its offline-first capabilities, mobile money integration, AI fact-checking, and hyperlocal communities. This combination makes it a powerful tool for connecting with others and sharing content.",
                "Zoomer africa is privacy focused platform that allows users to connect with others in their local communities. It offers features like offline-first mode, mobile money integration, AI fact-checking, and hyperlocal communities, making it a unique social networking experience."
            ],
            r"(?i).*zoomer ai.*|.*zoomer assistant.*|.*zoomer chatbot.*": [
                "Zoomer AI is your virtual assistant on Zoomer Africa. It helps you navigate the app, answer questions, and provide support. If you have any questions, feel free to ask!",
                "Zoomer AI is your virtual assistant on Zoomer Africa. It helps you navigate the app, answer questions, and provide support. If you have any questions, feel free to ask!"
            ],
            r"(?i).*about zoomer.*|.*what is zoomer africa.*|.*zoomer app.*": [
                "Zoomer Africa is a social networking platform designed for local communities. It offers features like offline-first mode, mobile money integration, AI fact-checking, and hyperlocal communities.",
                "Zoomer Africa is a social networking platform that focuses on connecting users within their local communities. It offers features like offline-first mode, mobile money integration, AI fact-checking, and hyperlocal communities."
            ],
            r"(?i).*zoomer languages.*|.*zoomer translation.*|.*zoomer auto-translate.*": [
                "Zoomer Africa supports multiple languages and offers auto-translate features to help users communicate across language barriers. You can enable this feature in the app settings.",
                "The app supports multiple languages and offers auto-translate features to help users communicate across language barriers. You can enable this feature in the app settings."
            ],
            r"(?i).*zoomer communities.*|.*zoomer groups.*|.*zoomer local communities.*": [
                "Zoomer Africa allows you to connect with local communities through groups and events. You can join or create groups based on your interests and location.",
                "You can connect with local communities on Zoomer Africa by joining or creating groups based on your interests and location."
            ],
            r"(?i).*zoomer slang.*|.*zoomer lingo.*|.*zoomer language.*": [
                "Zoomer slang refers to the unique language and expressions used by the Zoomer generation. It often includes internet slang, memes, and cultural references. If you have specific terms in mind, feel free to ask!",
                "Zoomer slang is a collection of unique expressions and terms used by the Zoomer generation. It often includes internet slang, memes, and cultural references. If you have specific terms in mind, feel free to ask!"
            ],
            r"(?i).*does zoomer have slang languages.*|.*zoomer humor.*|.*zoomer jokes.*": [
                "Zoomer humor often includes memes, internet culture references, and playful language. If you have specific jokes or terms in mind, feel free to ask!",
                "Zoomer humor is characterized by memes, internet culture references, and playful language. If you have specific jokes or terms in mind, feel free to ask!"
            ],
            r"(?i).*zoomer memes.*|.*zoomer culture.*|.*zoomer trends.*": [
                "Zoomer memes often reflect current trends, internet culture, and social issues. If you have specific memes or trends in mind, feel free to ask!",
                "Zoomer memes are a reflection of current trends, internet culture, and social issues. If you have specific memes or trends in mind, feel free to ask!"
            ],
            r"(?i).*zoomer news.*|.*zoomer updates.*|.*zoomer trends.*": [
                "Zoomer Africa provides updates on current trends, news, and events relevant to the Zoomer generation. You can find this information in the app's news section.",
                "You can find updates on current trends, news, and events relevant to the Zoomer generation in the app's news section."
            ],
            r"(?i).*zoomer events.*|.*zoomer happenings.*|.*zoomer activities.*": [
                "Zoomer Africa hosts various events and activities for users to participate in. You can find information about upcoming events in the app's events section.",
                "You can find information about upcoming events and activities in the app's events section."
            ],
            r"(?i).*zoomer challenges.*|.*zoomer competitions.*|.*zoomer contests.*": [
                "Zoomer Africa hosts various challenges and competitions for users to participate in. You can find information about upcoming challenges in the app's events section.",
                "You can find information about upcoming challenges and competitions in the app's events section."
            ],
            r"(?i).*zoomer rewards.*|.*zoomer points.*|.*zoomer achievements.*": [
                "Zoomer Africa offers rewards and points for participating in challenges, events, and activities. You can check your rewards status in the app's profile section.",
                "You can check your rewards and points status in the app's profile section."
            ],

        }


    
    def save_message(self, role, content):
        """Save messages to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_response(self, user_input):
        """Generate a response based on user input"""
        # Save user input to history
        self.save_message("user", user_input)
        
        # Check for empty input
        if not user_input.strip():
            response = "I noticed you sent an empty message. How can I help you with Zoomer Africa today?"
            self.save_message("assistant", response)
            return response
        
        # Check if user is greeting
        if re.match(r"(?i)hello|hi|hey|greetings", user_input):
            response = random.choice(self.greetings)
            self.save_message("assistant", response)
            return response
        
        # Check if user is saying goodbye
        if re.match(r"(?i)bye|goodbye|exit|quit", user_input):
            response = random.choice(self.farewells)
            self.save_message("assistant", response)
            return response
        
        # Check knowledge base for matches
        for pattern, responses in self.knowledge_base.items():
            if re.search(pattern, user_input):
                response = random.choice(responses)
                self.save_message("assistant", response)
                return response
        
        # Special handling for specific queries
        if "date" in user_input.lower():
            response = f"Today is {self.current_date}."
            self.save_message("assistant", response)
            return response
        
        # Generic response for unknown queries
        response = random.choice(self.unknown_responses)
        self.save_message("assistant", response)
        return response


# Create an instance of the chatbot
assistant = AfroZoomerAssistant()

@app.route('/')
def index():
    return render_template('zoomer_ai.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = assistant.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=8080)