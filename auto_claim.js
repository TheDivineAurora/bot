// auto_claim.js

const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const owner = process.env.GITHUB_REPO_OWNER; // GitHub username or organization
const repo = process.env.GITHUB_REPO_NAME; // GitHub repository name
const issueNumber = process.argv[2];

const githubToken = process.env.GITHUB_TOKEN;

if (!issueNumber) {
  console.error('Issue number not provided. Usage: node auto_claim.js <issue_number>');
  process.exit(1);
}

const comment = 'claim';

async function claimIssue() {
  try {
    // Add a comment to the issue using GitHub REST API
    const response = await axios.post(
      `https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}/comments`,
      { body: comment },
      {
        headers: {
          Authorization: `Bearer ${githubToken}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 201) {
      console.log(`Successfully claimed issue ${issueNumber}.`);
    } else {
      console.error(`Failed to claim issue ${issueNumber}. Status code: ${response.status}`);
    }
  } catch (error) {
    console.error('Error claiming issue:', error.message);
  }
}

claimIssue();
