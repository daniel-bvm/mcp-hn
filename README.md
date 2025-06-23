# Hacker News Agent

An AI assistant that provides the ability to fetch information from Hacker News.

## Tools

- `get_stories`: Fetching (top, new, ask_hn, show_hn) stories
- `get_story_info`: Fetching comments associated with a story
- `search_stories`: Searching for stories by query
- `get_user_info`: Fetching user info

## Example Usage

Use prompts like the following:

```
User: Get the top stories of today
  Output: Uses `get_stories` tool and returns a story about AI
User: What does the details of the story today that talks about the future of AI
  Output: Uses `get_story_info` tool based on the results of the previous tool
User: What has the user `pg` been up to?
  Output: Uses `get_user_info` tool and returns a summary of the user's activity
User: What does hackernews say about careers in AI?
  Output: Uses `search_stories` tool and returns a summary of the comments
```
