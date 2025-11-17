import mysql.connector
from mysql.connector import Error
import pandas as pd
from db.scripts.config import VEPKAR_DB, VEKPLAY_DB
from db.scripts.utils.helpers import execute_query, save_to_csv

def export_top_lemmas():
    vepkar_conn = None
    vekplay_conn = None
    
    try:
        # Connect to VepKar
        vepkar_conn = mysql.connector.connect(**VEPKAR_DB)
        
        # Query top lemmas with examples, audio and illustrations
        query = """
        SELECT
            l.id, l.lemma,
            COUNT(DISTINCT st.id) AS example_count,
            COUNT(DISTINCT al.audio_id) AS audio_count,
            COUNT(DISTINCT med.id) AS media_count
        FROM
            lemmas l
        LEFT JOIN audio_lemma al ON l.id = al.lemma_id
        LEFT JOIN media med ON l.id = med.model_id AND med.model_type = 'lemma'
        JOIN meanings m ON l.id = m.lemma_id
        JOIN meaning_text mt ON m.id = mt.meaning_id
        JOIN sentence_translations st ON mt.text_id = st.text_id
        GROUP BY l.id, l.lemma
        HAVING COUNT(st.id) > 0 OR COUNT(DISTINCT al.audio_id) > 0 OR COUNT(DISTINCT med.id) > 0
        ORDER BY example_count DESC, audio_count DESC, media_count DESC
        LIMIT 1000;
        """
        
        # Execute query
        top_lemmas = pd.read_sql(query, vepkar_conn)
        vepkar_conn.close()
        vepkar_conn = None
        
        # Save to CSV
        save_to_csv(top_lemmas, "share/data/lemmas.csv")
        
        # Connect to VekPlay and write data
        vekplay_conn = mysql.connector.connect(**VEKPLAY_DB)
        for _, row in top_lemmas.iterrows():
            insert_query = """
            INSERT INTO lemmas (id, lemma, example_count, audio_count, media_count)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                lemma = VALUES(lemma),
                example_count = VALUES(example_count),
                audio_count = VALUES(audio_count),
                media_count = VALUES(media_count);
            """
            execute_query(vekplay_conn, insert_query, row.tolist())
        
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
