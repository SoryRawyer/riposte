### riposte — turn TODO comments into github issues

### Usage
Configure a github webhook to send push events to https://nameless-mountain-59891.herokuapp.com/payload

Riposte will:
- get all TODO issues for a repo
- download all changed files
- parse out TODO comments via regex
- compute SHA1 hash of each comment
- if the hash is already present, don't make a new issue
- otherwise, create a new issue with the TODO statement as the title and the hash as the body

Deployed to Heroku at https://nameless-mountain-59891.herokuapp.com/

### FAQ
Q: what github user does this run as?  
A: [ripostebot](https://github.com/ripostebot)  
Q: what permissions does this need?  
A: Issues: read/write; issue labels: read/write; repo contents: read  
Q: Why "riposte"?  
A: It was the Merriam-Webster word of the day when I started this project.

