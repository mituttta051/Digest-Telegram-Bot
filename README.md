<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/assets/photo_2024-07-08_21.41.28.jpeg">
    <img src="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/raw/main/assets/photo_2024-07-08_21.41.28.jpeg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Digest Telegram Bot</h3>

  <p align="center">
    Generate digests for your Tg-channel in several seconds!
    <!-- <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <a href="https://www.youtube.com/watch?v=WjtujibU20U">View Demo</a>
    ·
    <a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/issues/new">Report Bug</a>
    ·
    <a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/issues/new">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#team-49">Team 49</a>
      <ul></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/assets/IMG_1855.jpg">
    <img src="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/raw/main/assets/IMG_1855.jpg" alt="Project Logo" width="180" height="">
</a>
<a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/assets/IMG_1867.jpg">
    <img src="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/raw/main/assets/IMG_1867.jpg" alt="Project Logo" width="180" height="">
</a>
<a href="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/assets/IMG_1866.jpg">
    <img src="https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/raw/main/assets/IMG_1866.jpg" alt="Project Logo" width="180" height="">
</a>



During the Software Project course in Innopolis University [Team 49](#team-49) has collaborated with customer Gleb Shamilov to create a Digest Telegram Bot that generates digests of channel posts using LLM. 

Key features 🌟:
* Digest period (week, 2 weeks, month, custom) 
* Channel selection 
* Main digest language (Ru/Eng) 
* Second digest language (Ru/Eng/none) 
* Bot language (Ru/Eng)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The DigestTelegramBot was built using:

* [![Python][Python.js]][Python-url]
* [![Aiogram][Aiogram.js]][Aiogram-url]
* [![SQLite][SQLite.js]][SQLite-url]
* [![YaGPT][YaGPT.js]][YaGPT-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


Follow these simple steps to get a local copy up and run it on your machine! 📦

### Prerequisites

* Python 3.10 or higher;
* Telegram account;
* git installed;
* pip (Python package installer) installed.
* Bot created in @BotFather.

### Installation

Copy and paste it to your terminal.

1. Clone the repo.
   ```sh
   git clone https://gitlab.pg.innopolis.university/i.ershov/digestBot.git
   ```
2. Create a virtual inviroment.
   ```sh
   python3 -m venv venv
   ```
3. Activate the virtual environment.
* For Windows:
   ```txt
   venv\Scripts\activate
   ```
* For macOS and Linux:
   ```sh
   source venv/bin/activate
   ```   
4. Install the required packages.
```sh
   pip install -r requirements.txt
   ```
5. Configure environment variables

Create a .env file in the project root directory and add your Telegram bot token (is given in a message after creation by @BotFather):
```sh
   BOT_TOKEN=your_telegram_bot_token

   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run the bot, use the following command:

```sh
   python run_bot.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Set up a bot
- [x] Create the landing message for the bot
- [x] Make the bot read messages
- [x] Integrate LLM
- [x] Make the bot send summaries to the channel
- [x] Configure and deploy the server for the bot operations
- [x] Implement Button Instructions for Enhanced Telegram Bot UX
- [x] Implement Databases for Telegram channels
- [x] Create Telegram channels and start Testing
- [x] Implement Databases for Telegram channels
- [x] Implement secure bot admin verification
- [x] Set up inviroment variables
- [x] Design database for channel posts
- [x] Implement customisable settings
- [x] Customise interface language
  - [x] Russian
  - [x] English
  - [ ] Others
- [x] Enable option to add personal LLM API Key
- [x] Configure language of posts in the channel
- [x] Add variety of digests periods
- [x] Add second language in digest
- [x] Add preview text for the digest
- [x] Deploy the new version
- [ ] Add automatic digest publishing
- [ ] Switch to free LLM
- [ ] Add ability of user to change prompt
- [ ] Implement monetization
- [ ] Create donate button



See the [open issues](https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- HOW TO CONTRIBUTE -->
## Contributing
1. Fork the repository (click the "Fork" button in the upper-right corner of the repository page.)
2. Create a new branch.
```sh
   git checkout -b feature/your-feature-name
   ```
3. Stash files with changes.
  * Some files:
   ```sh
   git add path/to/your/file1.py path/to/your/file2.py

   ```
  * All files:
  ```sh
   git add .
   ```

3. Commit staged files.
```sh
   git commit -m 'Add some feature'
   ```
4. Push to the branch.
```sh
   git push origin feature/your-feature-name
   ```
5. Open a pull request (In repository page: Merge Requests -> New merge request, select Source branch with changes, select Target branch to apply changes on, review changes, provide title and detailed description.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- TEAM MEMBERS -->
## Team 49
* Ivan Ershov - bot architect, project administrator, software engineer, techical support, contributor;
* Timur Salakhov - bot architect, database engineer, quality assurance engineer, contributor;
* Lana Ermolaeva - technical writer, prototype designer, contributor;
* Anastasia Mitiutneva - team coordinator, technical writer, prompt engineer, contributor;
* Ivan Makarov - videographer, tester, contributor;
* Anastasia Surikova - architectural documenter, tester, contributor.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ivan Ershov - [tg: @spiritonchic](https://t.me/spiritonchic) - i.ershov@innopolis.university

Project Link: [https://gitlab.pg.innopolis.university/i.ershov/digestBot](https://gitlab.pg.innopolis.university/i.ershov/digestBot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Here are several credits by [Team 49](#team-49).

* [Innopolis University](https://innopolis.university)
* [Product Hunt Daily tg channel @ph_daily](https://t.me/ph_daily)
* [GitLab documentation](https://docs.gitlab.com)
* [Iogram full course on Russian](https://www.youtube.com/playlist?list=PLV0FNhq3XMOJ31X9eBWLIZJ4OVjBwb-KM)
* [Iogram documentation](https://docs.aiogram.dev/en/latest/)
* [SQLite documentation](https://www.sqlite.org/docs.html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/Contributors-lightblue?style=for-the-badge&color=41BAD5&link=https%3A%2F%2Fgitlab.pg.innopolis.university%2Fi.ershov%2FdigestBot%2F-%2Fgraphs%2Fmain%3Fref_type%3Dheads
[contributors-url]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/graphs/main?ref_type=heads
[forks-shield]: https://img.shields.io/badge/Forks-white?style=for-the-badge&color=F8F5F5&link=https%3A%2F%2Fgitlab.pg.innopolis.university%2Fi.ershov%2FdigestBot%2F-%2Fforks
[forks-url]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/forks
[stars-shield]: https://img.shields.io/badge/Starrers-white?style=for-the-badge&color=41BAD5&link=https%3A%2F%2Fgitlab.pg.innopolis.university%2Fi.ershov%2FdigestBot%2F-%2Fforks
[stars-url]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/starrers
[issues-shield]: https://img.shields.io/badge/Issues-white?style=for-the-badge&color=F8F5F5&link=https%3A%2F%2Fgitlab.pg.innopolis.university%2Fi.ershov%2FdigestBot%2F-%2Fissues
[issues-url]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/issues
[license-shield]: https://img.shields.io/badge/License-white?style=for-the-badge&color=41BAD5&link=https%3A%2F%2Fgitlab.pg.innopolis.university%2Fi.ershov%2FdigestBot%2F-%2Fblob%2Fmain%2FLICENSE%3Fref_type%3Dheads
[license-url]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/LICENSE?ref_type=heads
[product-screenshot]: https://gitlab.pg.innopolis.university/i.ershov/digestBot/-/blob/main/assets/IMG_1855.jpg
[Python.js]: https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white&link=https%3A%2F%2Fwww.python.org
[Python-url]: https://www.python.org
[Aiogram.js]: https://img.shields.io/badge/Aiogram-lightblue?style=for-the-badge&link=https%3A%2F%2Faiogram.dev
[Aiogram-url]: https://aiogram.dev
[SQLite.js]: https://img.shields.io/badge/SQLite-%23044a64?style=for-the-badge&link=https%3A%2F%2Fwww.sqlite.org
[SQLite-url]: https://www.sqlite.org
[YaGPT.js]: https://img.shields.io/badge/YaGPT-red?style=for-the-badge&logo=yandex&link=https%3A%2F%2Fya.ru%2Fai%2Fgpt-3
[YaGPT-url]: https://ya.ru/ai/gpt-3
