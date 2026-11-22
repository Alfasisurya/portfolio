# Marcelinus Alfasisurya Setya Adhiwibawa, M.Stat.

Plain HTML site. No npm, no Astro, and no build service.

Open `index.html` in a browser.

The pages are in English. They include the portrait, the Google Scholar citation record, LinkedIn, paper links, and the public NIR patent. Employer projects are described only in general terms.

## Publish on GitHub Pages

1. Create a repository and push this folder.
2. In Settings → Pages, set the source to the `main` branch and the folder `/ (root)`.
3. The site will be at `https://<user>.github.io/<repository>/`.

Links inside the pages are relative, so the same files work in a project site and when opened locally.

## Change the text

Edit the Markdown in `src/content`, then run:

```bash
python build_site.py
```

Python is used only to refresh the HTML. The published site does not need it.
