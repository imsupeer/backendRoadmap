# GitHub User Activity

Use GitHub API to fetch user activity and display it in the terminal.

In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.

# Requirements

The application should run from the command line, accept the GitHub username as an argument, fetch the user’s recent activity using the GitHub API, and display it in the terminal. The user should be able to:

- Provide the GitHub username as an argument when running the CLI.\
   github-activity username

- Fetch the recent activity of the specified GitHub user using the GitHub API. You can use the following endpoint to fetch the user’s activity:

    <p>
        https://api.github.com/users/username/events <br />
        Example: https://api.github.com/users/kamranahmedse/events
    </p>

- Display the fetched activity in the terminal.\
   Output: <br />
   <p>
   Pushed 3 commits to kamranahmedse/developer-roadmap <br />
   Opened a new issue in kamranahmedse/developer-roadmap <br />
   Starred kamranahmedse/developer-roadmap
  </p>

- Handle errors gracefully, such as invalid usernames or API failures.
- Use a programming language of your choice to build this project.
- Do not use any external libraries or frameworks to fetch the GitHub activity.
