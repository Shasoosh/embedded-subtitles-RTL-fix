# embedded-subtitles-RTL-fix

1. Inside Bazarr -> Settings -> Subtitles - untick "Reverse RTL"
2. Tick Custom Post-Processing 
3. `python3 /config/rev.py "{{subtitles}}" "{{subtitle_id}}"`
