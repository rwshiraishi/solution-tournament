# Diagram sources

The README diagrams are pre-rendered PNGs so they display identically in every
browser. GitHub's in-browser Mermaid renderer measures text in a different font
than it displays, which truncated node labels (differently in Chrome and Safari),
so client-side rendering was dropped entirely.

To edit a diagram, change its `.mmd` source here, then regenerate both theme
variants:

```bash
cd diagrams
for name in pipeline rounds; do
  npx -y -p @mermaid-js/mermaid-cli mmdc -i $name.mmd -o $name-light.png -b transparent -s 2
  npx -y -p @mermaid-js/mermaid-cli mmdc -i $name.mmd -o $name-dark.png -b transparent -s 2 -c dark-config.json
done
```

The README swaps variants automatically via `<picture>` and
`prefers-color-scheme`.
