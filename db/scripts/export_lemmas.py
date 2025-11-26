import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
from db.scripts.config import VEPKAR_DB, VEKPLAY_DB
from db.scripts.utils.helpers import execute_query, save_to_csv, save_to_json

def export_top_lemmas():
    vepkar_conn = None
    vekplay_conn = None
    
    try:
        # Connect to VepKar
        vepkar_conn = mysql.connector.connect(**VEPKAR_DB)
        
        # Create SQLAlchemy engine for Vepkar database
        vepkar_engine = create_engine(
            f"mysql+pymysql://{VEPKAR_DB['user']}:{VEPKAR_DB['password']}@{VEPKAR_DB['host']}/{VEPKAR_DB['database']}"
        )
        
        # Export all langs from VepKar to VekPlay
        langs_query = "SELECT id, name_en, name_ru, short_ru, code, sequence_number FROM langs"
        langs_df = pd.read_sql(langs_query, vepkar_engine)
        
        # Connect to VekPlay and insert langs
        vekplay_conn = mysql.connector.connect(**VEKPLAY_DB)
        for _, row in langs_df.iterrows():
            insert_lang_query = """
            INSERT INTO langs (id, name_en, name_ru, short_ru, code, sequence_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name_en = VALUES(name_en),
                name_ru = VALUES(name_ru),
                short_ru = VALUES(short_ru),
                code = VALUES(code),
                sequence_number = VALUES(sequence_number);
            """
            params = (row['id'], row['name_en'], row['name_ru'], row['short_ru'], row['code'], row['sequence_number'])
            execute_query(vekplay_conn, insert_lang_query, params)
        
        # Save langs to JSON file
        langs_json = []
        for _, row in langs_df.iterrows():
            lang_data = {
                'id': int(row['id']),
                'name_en': row['name_en'],
                'name_ru': row['name_ru'],
                'short_ru': row['short_ru'],
                'code': row['code'],
                'sequence_number': int(row['sequence_number'])
            }
            langs_json.append(lang_data)
        
        save_to_json(langs_json, "share/data/langs.json")
        
        # Query top lemmas with examples, audio and illustrations
        query = """
        SELECT
            l.id, l.lemma, l.lang_id,
            COUNT(DISTINCT st.id) AS example_count,
            COUNT(DISTINCT al.audio_id) AS audio_count,
            COUNT(DISTINCT med.id) AS media_count
        FROM
            lemmas l
        LEFT JOIN audio_lemma al ON l.id = al.lemma_id
        LEFT JOIN media med ON l.id = med.model_id AND med.model_type = 'lemma'
        JOIN meanings m ON l.id = m.lemma_id
        JOIN meaning_text mt ON m.id = mt.meaning_id
        JOIN sentences s ON mt.text_id = s.text_id
        JOIN sentence_translations st ON s.id = st.sentence_id
        GROUP BY l.id, l.lemma, l.lang_id
        HAVING COUNT(st.id) > 0 OR COUNT(DISTINCT al.audio_id) > 0 OR COUNT(DISTINCT med.id) > 0
        ORDER BY example_count DESC, audio_count DESC, media_count DESC
        LIMIT 7;
        """
        
        # Create SQLAlchemy engine for Vepkar database
        vepkar_engine = create_engine(
            f"mysql+pymysql://{VEPKAR_DB['user']}:{VEPKAR_DB['password']}@{VEPKAR_DB['host']}/{VEPKAR_DB['database']}"
        )
        
        # Execute query
        top_lemmas = pd.read_sql(query, vepkar_engine)
        vepkar_conn.close()
        vepkar_conn = None
        
        # Save to CSV
        save_to_csv(top_lemmas, "share/data/lemmas.csv")
        
        # Save to JSON file for React app
        lemmas_json = []
        for _, row in top_lemmas.iterrows():
            lemma_data = {
                'id': int(row['id']),
                'lemma': row['lemma'],
                'lang_id': int(row['lang_id']),
                'example_count': int(row['example_count']),
                'audio_count': int(row['audio_count']),
                'media_count': int(row['media_count'])
            }
            lemmas_json.append(lemma_data)
        
        save_to_json(lemmas_json, "share/data/lemmas.json")
        
        # Connect to VekPlay and write only basic lemma data (without counts)
        vekplay_conn = mysql.connector.connect(**VEKPLAY_DB)
        for _, row in top_lemmas.iterrows():
            insert_query = """
            INSERT INTO lemmas (id, lemma, lang_id, lemma_for_search)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                lemma = VALUES(lemma),
                lang_id = VALUES(lang_id),
                lemma_for_search = VALUES(lemma_for_search);
            """
            # Use the lemma itself as lemma_for_search if no other logic is defined
            params = (row['id'], row['lemma'], row['lang_id'], row['lemma'])
            execute_query(vekplay_conn, insert_query, params)
        
        print(f"Export completed successfully. Processed {len(top_lemmas)} lemmas.")
        
    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except pd.errors.EmptyDataError:
        print("Error: received empty data")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if vepkar_conn and vepkar_conn.is_connected():
            vepkar_conn.close()
        if vekplay_conn and vekplay_conn.is_connected():
            vekplay_conn.close()

if __name__ == "__main__":
    export_top_lemmas()
