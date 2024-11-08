# OG Image Grabber

A lightweight utility to extract OpenGraph images and descriptions from web pages. Perfect for generating link previews in newsletters, content aggregators, or any application that needs to display rich link previews.

## Features

- Extract OpenGraph images from web pages
- Fetch page descriptions (OpenGraph or meta descriptions)
- Fallback mechanisms for when OG tags are not available
- Easy to use API
- No external dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Create a file named `urls.txt` with the URLs you want to process, one per line.
2. Run the script:

```bash
python main.py
```

The files will be saved in the `dist` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Creative Commons Zero v1.0 Universal license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for simple OpenGraph data extraction
- Built with ❤️ for the open source community
