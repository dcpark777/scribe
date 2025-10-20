# Documentation Deployment Guide

This guide covers how to deploy Scribe's documentation to various platforms.

## 🎯 Recommended: Read the Docs

**Read the Docs** is the most popular choice for Python project documentation.

### Setup Steps:

1. **Create Read the Docs account:**
   - Go to [readthedocs.org](https://readthedocs.org)
   - Sign up with your GitHub account

2. **Import your project:**
   - Click "Import a Project"
   - Select your `scribe` repository
   - Choose "Read the Docs" as the documentation type

3. **Configure build settings:**
   - The `.readthedocs.yml` file is already configured
   - Set Python version to 3.11
   - Enable "Install Project" if you want to test imports

4. **Build and deploy:**
   - Click "Build version" to test
   - Documentation will be available at `https://data-scribe.readthedocs.io`

### Custom Domain (Optional):
- Go to Admin → Domains
- Add your custom domain (e.g., `docs.scribe.dev`)
- Update DNS records as instructed

## 🌐 GitHub Pages

**GitHub Pages** provides free hosting directly from your repository.

### Setup Steps:

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"

2. **Deploy automatically:**
   - The `.github/workflows/docs.yml` workflow is already configured
   - Push to `main` branch to trigger deployment
   - Documentation will be available at `https://yourusername.github.io/scribe`

3. **Custom domain (Optional):**
   - Add your domain in repository Settings → Pages
   - Create a `CNAME` file with your domain name

## 🚀 Netlify

**Netlify** offers excellent performance and easy deployment.

### Setup Steps:

1. **Connect to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Sign up and connect your GitHub account

2. **Deploy from Git:**
   - Click "New site from Git"
   - Select your `scribe` repository
   - Build settings are pre-configured in `netlify.toml`

3. **Deploy:**
   - Netlify will automatically build and deploy
   - Documentation will be available at `https://random-name.netlify.app`

4. **Custom domain (Optional):**
   - Go to Site settings → Domain management
   - Add your custom domain

## ☁️ Vercel

**Vercel** provides fast global CDN and excellent performance.

### Setup Steps:

1. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up and connect your GitHub account

2. **Import project:**
   - Click "New Project"
   - Select your `scribe` repository
   - Build settings are pre-configured in `vercel.json`

3. **Deploy:**
   - Vercel will automatically build and deploy
   - Documentation will be available at `https://scribe.vercel.app`

4. **Custom domain (Optional):**
   - Go to Project settings → Domains
   - Add your custom domain

## 🔧 Local Testing

Before deploying, test your documentation locally:

```bash
# Build documentation
make docs

# Serve locally
make docs-serve

# Open in browser
open http://localhost:8000
```

## 📝 Deployment Checklist

- [ ] Documentation builds successfully locally
- [ ] All links work correctly
- [ ] Search functionality works
- [ ] Mobile responsive design
- [ ] Custom domain configured (if desired)
- [ ] Analytics tracking set up (if desired)

## 🎨 Customization

### Theme Customization:
- Edit `docs/source/conf.py` to change theme settings
- Add custom CSS in `docs/source/_static/`

### Content Updates:
- Edit `.rst` files in `docs/source/`
- Rebuild and redeploy

### SEO Optimization:
- Update `docs/source/conf.py` with proper metadata
- Add sitemap and robots.txt if needed

## 🚨 Troubleshooting

### Common Issues:

1. **Build failures:**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Review build logs for specific errors

2. **Missing content:**
   - Ensure all files are committed to repository
   - Check file paths and references

3. **Styling issues:**
   - Verify theme is properly installed
   - Check CSS file paths

### Support:
- Read the Docs: [docs.readthedocs.io](https://docs.readthedocs.io)
- GitHub Pages: [docs.github.com/pages](https://docs.github.com/pages)
- Netlify: [docs.netlify.com](https://docs.netlify.com)
- Vercel: [vercel.com/docs](https://vercel.com/docs)
