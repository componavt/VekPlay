#!/bin/bash
#
# Script to dump VepKar database tables required for VekPlay project.
# Asks for user credentials, generates a dump file with the current date,
# and compresses the dump using zstd.

# Ask for user credentials
read -p "Enter MariaDB username: " user_name
read -s -p "Enter MariaDB password: " password
echo

# Generate filename with current date
current_date=$(date +"%Y%m%d")
dump_file="vekplay-$current_date.sql"
compressed_file="$dump_file.zst"

# Execute mysqldump with provided credentials and save to the generated filename
sudo mysqldump -u "$user_name" -p"$password" --default-character-set=utf8mb4 --single-transaction --skip-comments \
--skip-add-drop-table --skip-lock-tables --skip-disable-keys vepkar \
concepts concept_categories concept_meaning meanings lemmas meaning_text langs parts_of_speech places meaning_place \
dialects dialect_place dialect_lemma dialect_meaning dialect_phonetic labels label_lemma label_meaning lemma_features \
lemma_variants meaning_relation meaning_synset meaning_translation media audio_lemma audios phonetic_place relations \
sentence_translations synsets syntypes > "$dump_file"

# Compress the dump file using zstd
zstd -19 -T0 "$dump_file"

# Notify user about the completion
echo "Database dump completed and compressed. Original file: $dump_file, Compressed file: $compressed_file"
