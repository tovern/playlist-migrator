import argparse
import sys
from provider import Provider


def main():
    parser = argparse.ArgumentParser(description='Import or export playlist data from a streaming music provider')

    # Required arguments
    parser.add_argument('provider', choices=['spotify', 'youtube'], help='Specify the streaming music provider (spotify or youtube)')
    parser.add_argument('action', choices=['import', 'export'], help='Specify the action to perform (import or export)')

    # Optional argument
    # parser.add_argument('--playlist', help='Specify the playlist name (optional)')

    args = parser.parse_args()

    # Access the values using args.provider, args.action, and args.playlist
    print(f"Provider: {args.provider}")
    print(f"Action: {args.action}")

    streaming_provider = Provider()
    init_method = getattr(streaming_provider, f'{args.provider}_init')
    init_method()

    if args.action == "export":
        fetch_method = getattr(streaming_provider, f'{args.provider}_fetch_tracks')
        fetch_method()
        streaming_provider.export_tracks()
    elif args.action == "import":
        streaming_provider.import_tracks()
        add_method = getattr(streaming_provider, f'{args.provider}_add_tracks')
        add_method()


if __name__ == "__main__":
    main()