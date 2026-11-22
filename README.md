# Marcelinus Alfasisurya Setya Adhiwibawa, M.Stat.

Plain HTML site. No npm, no Astro, and no build service.

Open `index.html` in a browser.

The pages are in English. They include the portrait, the Google Scholar citation record, LinkedIn, paper links, and the public NIR patent. Employer projects are described only in general terms.

## Publish on GitHub Pages

1. Create a repository and push this folder.
2. In Settings → Pages, set the source to the `main` branch and the folder `/ (root)`.
3. The site will be at `https://<user>.github.io/<repository>/`.

Links inside the pages are relative, so the same files work in a project site and when opened locally.

## Write a blog post

1. Copy `templates/blog.md` to `src/content/blog/`, and give it a short file name such as `my-new-post.md`. The file name becomes the web address: `blog/my-new-post/`.
2. Fill in the title, date (`YYYY-MM-DD`), topics, and summary at the top, then write the post below the second `---` line.
3. Images go in `public/images/blog/`.
4. Run `python build_site.py`, open `blog.html` to check, then commit and push.

Posts are listed newest first on the Blog page, and the three newest also appear on the home page.

## Change the text

Edit the Markdown in `src/content`, then run:

```bash
python build_site.py
```

Python is used only to refresh the HTML. The published site does not need it.
