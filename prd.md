
# Docling Container

I want to create a docker container that runs docling, a documentation conversion tool for a variety of document formats.

## Docling

- Documentation for docling can be found at https://docling-project.github.io/docling/getting_started/
- I want to invoke docling using Python to drive the conversion process.
- Use uv as the package manager.

## Conversion Format

- Docling should input documents in the following formats :
    - HTML
    - Markdown
    - Microsoft Word (.docx)
    - Microsoft PowerPoint (.pptx)
    - Microsoft Excel (.xlsx)
    - PDF
    - ASCIIDOC
    - CSV
    - PNG, JPEG, TIFF, BMP, WEBP

- Docling should output documents in the following formats:
    - HTML
    - Markdown
    - JSON
    - Text
    - Doctags

- Docling should support batch processing of multiple files in a single run.

- Docling should preserve the original formatting and structure of the documents as much as possible during conversion.

- Docling should handle errors gracefully and provide meaningful error messages when conversion fails.

- Docling should log the conversion process, including start and end times, number of files processed, and any errors encountered.

- Docling should be configurable via command line arguments or a configuration file to specify input and output formats, directories, and other options.

- Docling should be optimized for performance to handle large documents and multiple files efficiently.

- Docling should be tested with a variety of document types and formats to ensure reliability and accuracy of conversions.

- Docling should have a help command or documentation accessible from the command line to guide users on how to use the tool.

- Docling should have options to enable or disable specific features, such as logging verbosity, error handling behavior, and output formatting options.

## Container

- The container should be based on Python 3.13.
- The container should be small and efficient - use a multistage build.
    - Use uv in the first stage to install docling and dependencies
- The container should support a mount for an input directory and an output directory.
- The container should expose a command line interface to run docling conversions.
- The container should have proper error handling and logging. 


## Documentation

- Provide clear instructions on how to build and run the container.
- Include examples of how to use the container to convert documents.
- Document any configuration options available for docling within the container.    
- Include troubleshooting tips for common issues that may arise when using the container.
- Include examples of command line invocations for different conversion scenarios.

