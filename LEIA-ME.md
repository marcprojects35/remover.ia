# AI Audio Fingerprint Remover

Remove fingerprints e marcas d'água de áudios gerados por IA (Suno, ElevenLabs, OpenAI, etc.).

## O que faz

- Remove todos os metadados (ID3, RIFF, tags customizadas)
- Detecta e remove watermarks espectrais (frequências altas, padrões periódicos)
- Normaliza padrões estatísticos gerados por máquina
- Adiciona imperfeições humanas sutis (micro-variações de timing, dinâmica, fase)
- Suporta: MP3, WAV, FLAC, AIFF

## Como abrir

```bash
./abrir_interface.sh
```

Ou clique duplo em `abrir_interface.sh`.

## Níveis de processamento

| Nível | O que faz |
|---|---|
| `gentle` | Mínimo — preserva qualidade, pode deixar alguns fingerprints |
| `moderate` | Balanceado — bom equilíbrio (padrão do script original) |
| `aggressive` | Remove a maioria dos fingerprints, qualidade ok ← **recomendado** |
| `extreme` | Remove tudo, pode adicionar artefatos sutis |

## Linha de comando (sem interface)

```bash
# arquivo único
./venv/bin/python ai_audio_fingerprint_remover.py entrada.mp3 saida.mp3 --level aggressive

# pasta inteira
./venv/bin/python ai_audio_fingerprint_remover.py --directory pasta_entrada pasta_saida --level aggressive
```

## Dependências

Já instaladas no `venv/`. Não precisa instalar nada mais.

## Fonte

https://github.com/geeknik/ai-audio-fingerprint-remover
