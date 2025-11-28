"""seed_local_data

Revision ID: 92aad8a1353b
Revises: f35327670f79
Create Date: 2025-11-27 22:41:37.812651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '92aad8a1353b'
down_revision: Union[str, Sequence[str], None] = 'f35327670f79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed database with books and clubs from local development environment."""

    # Note: This migration uses raw SQL with ON CONFLICT to make it idempotent
    # It will not overwrite existing data, only insert if the record doesn't exist
    # Admin user/role is already seeded in migration 379a81d365b7

    # Use text() to ensure proper execution with asyncpg
    # Each execute() call must contain only ONE SQL statement

    # ========== SEED BOOKS ==========
    conn = op.get_bind()

    # Book 1: The idiot
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '66027c3f-71e3-4e69-afbf-0b4f103c1c87'::uuid,
            'The idiot',
            'Fyodor Dostoevsky',
            '1875-02-24'::date,
            'Russian Literature',
            'Originally published: New York : Macmillan, 1913.',
            'https://covers.openlibrary.org/b/isbn/1853261750-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T14:38:43.281701'::timestamp,
            '2025-11-24T15:13:22.074425'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 2: The Brothers Karamazov
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'baae5ef4-5315-4240-940d-f853c0a53cc7'::uuid,
            'The Brothers Karamazov',
            'Fyodor Dostoevsky',
            '2005-01-01'::date,
            'Russian Literature',
            'Originally published: New York : Macmillan, 1912.',
            'https://covers.openlibrary.org/b/id/14302295-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T14:49:13.385899'::timestamp,
            '2025-11-24T15:39:09.381302'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 3: Crime and punishment
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '12f3da9d-9ef4-4c0f-bde1-839a0e20eebf'::uuid,
            'Crime and punishment',
            'Fyodor Dostoevsky',
            '2015-01-01'::date,
            'Russian Literature',
            'Includes bibliographical references.',
            'https://covers.openlibrary.org/b/id/12775580-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T14:50:36.678767'::timestamp,
            '2025-11-24T15:38:47.675519'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 4: Reformed dogmatics Vol. 1
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '4e128b87-9aae-4750-ad0b-b2a630668c01'::uuid,
            'Reformed dogmatics Vol. 1: Prolegomena',
            'Bavinck, Herman, Herman Bavinck, John Bolt, John Vriend',
            '2003-01-01'::date,
            'Theology',
            'Includes bibliographical references and indexes.',
            'https://covers.openlibrary.org/b/id/13023039-L.jpg',
            'Reformed dogmatics',
            1,
            'Prolegomena',
            '2025-11-24T14:55:47.920964'::timestamp,
            '2025-11-24T16:08:31.121132'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 5: Reformed dogmatics Vol. 3
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'b211b195-451b-495b-8698-d02631796d28'::uuid,
            'Reformed dogmatics Vol. 3: God and Creation',
            'Bavinck, Herman, Herman Bavinck, John Bolt, John Vriend',
            '2003-01-01'::date,
            'Theology',
            'Includes bibliographical references and indexes.',
            'https://covers.openlibrary.org/b/id/13023039-L.jpg',
            'Reformed dogmatics',
            2,
            'God and creation',
            '2025-11-24T16:02:31.991186'::timestamp,
            '2025-11-24T16:02:50.207854'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 6: Reformed dogmatics Vol. 3: Sin and salvation
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'c4be25ec-f112-4cf5-a23f-3a77c5361208'::uuid,
            'Reformed dogmatics Vol. 3: Sin and salvation in Christ',
            'Bavinck, Herman, Herman Bavinck, John Bolt, John Vriend',
            '2003-01-01'::date,
            'Theology',
            'Includes bibliographical references and indexes.',
            'https://covers.openlibrary.org/b/id/13023039-L.jpg',
            'Reformed dogmatics',
            3,
            'Sin and salvation in Christ',
            '2025-11-24T16:06:28.011865'::timestamp,
            '2025-11-24T16:06:28.011871'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 7: Reformed dogmatics Vol. 4
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '0aecfc31-f024-46cd-a316-c584cd3c3104'::uuid,
            'Reformed dogmatics Vol. 4: Holy Spirit, church, and new creation.',
            'Bavinck, Herman, Herman Bavinck, John Bolt, John Vriend',
            '2003-01-01'::date,
            'Theology',
            'Includes bibliographical references and indexes.',
            'https://covers.openlibrary.org/b/id/13023039-L.jpg',
            'Reformed dogmatics',
            4,
            'Holy Spirit, church, and new creation.',
            '2025-11-24T16:07:12.237143'::timestamp,
            '2025-11-24T16:07:12.237148'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 8: Anna Karenina
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'a77726b0-c467-415c-b41e-8d5070e85b7e'::uuid,
            'Anna Karenina',
            'Leo Tolstoy',
            '2001-01-01'::date,
            'Russian Literature',
            'a novel in eight parts',
            'https://covers.openlibrary.org/b/id/402774-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T16:12:32.312424'::timestamp,
            '2025-11-24T16:12:32.312432'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 9: War and peace
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '522506f6-08ab-4acf-8112-b617c4668e65'::uuid,
            'War and peace',
            'Leo Tolstoy',
            '1992-01-01'::date,
            'Russian Literature',
            'Includes bibliographical references.
Translation of Voǐna i mir.',
            'https://covers.openlibrary.org/b/id/417336-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T16:14:08.662746'::timestamp,
            '2025-11-24T16:14:08.662757'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 10: Institutes of the Christian Religion
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '9414ee88-db1b-4819-8753-428723abeeb6'::uuid,
            'Institutes of the Christian Religion',
            'John Calvin',
            '2014-01-01'::date,
            'Reformed church, doctrines',
            'A new English translation from the 1541 French edition',
            'https://covers.openlibrary.org/b/id/7383446-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T16:32:48.080641'::timestamp,
            '2025-11-24T16:32:48.080649'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 11: The Space Trilogy
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'db667399-125e-4dc2-a485-327f5b79fc41'::uuid,
            'The Space Trilogy  by C.S. Lewis  Paperback',
            'C.S. Lewis',
            '2011-01-01'::date,
            'Fiction, science fiction, space opera',
            'Source title: The Space Trilogy (Out of the Silent Planet, Perelandra, That Hideous Strength) by C.S. Lewis (2011) Paperback',
            'https://covers.openlibrary.org/b/id/9102561-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T21:52:38.672536'::timestamp,
            '2025-11-24T21:52:38.672543'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 12: Existence and Attributes of God
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'afe9679d-8fe4-48d7-9d96-3d01eec16019'::uuid,
            'Existence and Attributes of God',
            'Stephen Charnock, Mark Jones',
            '2022-01-01'::date,
            'Theology, doctrinal',
            'Updated and Unabridged',
            'https://covers.openlibrary.org/b/id/14753764-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T21:56:37.095258'::timestamp,
            '2025-11-24T21:56:37.095264'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 13: Covenant Theology
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '4204cbb3-6b72-473e-9ba2-31ad9912e6ff'::uuid,
            'Covenant Theology',
            'Guy Prentiss Waters',
            '2020-01-01'::date,
            'Theology',
            'Biblical, Theological, and Historical Perspectives',
            'https://covers.openlibrary.org/b/id/13307975-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:01:33.990747'::timestamp,
            '2025-11-24T22:01:33.990754'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 14: The Return of the King
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'd28c40a7-6844-4fad-9737-2f41a7b91c65'::uuid,
            'The Return of the King',
            'J.R.R. Tolkien',
            '1997-01-01'::date,
            'Fiction',
            'Being the third part of The Lord of the Rings',
            'https://covers.openlibrary.org/b/id/2341322-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:05:48.424624'::timestamp,
            '2025-11-24T22:05:48.424632'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 15: The Two Towers
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '1f97ab47-af1f-489a-b715-a1692044a9b6'::uuid,
            'The Two Towers',
            'J.R.R. Tolkien',
            '1997-01-01'::date,
            'Fantasy fiction',
            'UK / CAN edition',
            'https://covers.openlibrary.org/b/id/14624433-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:06:30.015597'::timestamp,
            '2025-11-24T22:06:30.015603'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 16: The Fellowship of the Ring
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '6275c348-fdf0-4aec-8418-51c0085135cc'::uuid,
            'The Fellowship of the Ring',
            'J.R.R. Tolkien',
            '2011-01-01'::date,
            'Fantasy Fiction',
            'The Lord of the Rings, Part I',
            'https://covers.openlibrary.org/b/id/11204800-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:07:04.582806'::timestamp,
            '2025-11-24T22:07:04.582812'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 17: The Hobbit
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            'ceb6ace8-4399-41e8-9cbd-938c42cd9a11'::uuid,
            'The Hobbit',
            'J.R.R. Tolkien',
            '2011-01-01'::date,
            'Fantasy Fiction',
            'UK',
            'https://covers.openlibrary.org/b/id/10522108-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:08:08.033511'::timestamp,
            '2025-11-24T22:08:08.033527'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # Book 18: The Silmarillion
    conn.execute(text("""
        INSERT INTO books (id, title, author, date_of_first_publish, genre, description, cover_image_url, series_title, volume_number, volume_title, created_at, updated_at)
        VALUES (
            '46f84d1b-f7aa-4858-aadf-b87a9e545eeb'::uuid,
            'The Silmarillion',
            'J.R.R. Tolkien',
            '1999-01-01'::date,
            'Fantasy fiction',
            '',
            'https://covers.openlibrary.org/b/id/12027840-L.jpg',
            NULL,
            NULL,
            NULL,
            '2025-11-24T22:10:15.413483'::timestamp,
            '2025-11-24T22:10:15.413489'::timestamp
        )
        ON CONFLICT (id) DO NOTHING
    """))

    # ========== SEED CLUBS ==========
    # Get admin user ID first
    result = conn.execute(text("SELECT id FROM users WHERE username = 'admin' LIMIT 1"))
    admin_user_row = result.fetchone()

    if admin_user_row:
        admin_user_id = admin_user_row[0]

        # Club 1: The Inklings
        conn.execute(text("""
            INSERT INTO clubs (id, name, description, topic, created_by, is_active, max_members, created_at, updated_at)
            VALUES (
                '777ebbb6-e083-4337-9539-62db50c63668'::uuid,
                'The Inklings',
                'A ground for the discussion of what is lovely, beautiful and genuinely Good.',
                'All encompassing',
                :admin_user_id,
                true,
                NULL,
                '2025-11-23T02:38:23.421079'::timestamp,
                '2025-11-23T02:38:23.421086'::timestamp
            )
            ON CONFLICT (id) DO NOTHING
        """), {"admin_user_id": admin_user_id})

        # Club 2: The Classics Crew
        conn.execute(text("""
            INSERT INTO clubs (id, name, description, topic, created_by, is_active, max_members, created_at, updated_at)
            VALUES (
                '1ab87609-068b-4990-b943-f4bcfcfe3604'::uuid,
                'The Classics Crew',
                'A club for the sole purpose of studying the wisdom of classic literature.',
                'Classic Literature',
                :admin_user_id,
                true,
                NULL,
                '2025-11-23T02:47:28.680076'::timestamp,
                '2025-11-23T02:47:28.680082'::timestamp
            )
            ON CONFLICT (id) DO NOTHING
        """), {"admin_user_id": admin_user_id})

        # Club 3: Mens Bible Study
        conn.execute(text("""
            INSERT INTO clubs (id, name, description, topic, created_by, is_active, max_members, created_at, updated_at)
            VALUES (
                '681ff682-f876-40d0-bfda-994197a879e1'::uuid,
                'Mens Bible Study',
                'A group of men gathering to indulge in the boundless truths of Gods Word.',
                'Theology',
                :admin_user_id,
                true,
                NULL,
                '2025-11-23T03:46:28.316326'::timestamp,
                '2025-11-23T03:46:28.316333'::timestamp
            )
            ON CONFLICT (id) DO NOTHING
        """), {"admin_user_id": admin_user_id})

        # Add admin to all clubs as member
        conn.execute(text("""
            INSERT INTO user_clubs (user_id, club_id, join_date, role)
            VALUES (
                :admin_user_id,
                '777ebbb6-e083-4337-9539-62db50c63668'::uuid,
                '2025-11-23T02:38:23.421079'::timestamp,
                'member'
            )
            ON CONFLICT DO NOTHING
        """), {"admin_user_id": admin_user_id})

        conn.execute(text("""
            INSERT INTO user_clubs (user_id, club_id, join_date, role)
            VALUES (
                :admin_user_id,
                '1ab87609-068b-4990-b943-f4bcfcfe3604'::uuid,
                '2025-11-23T02:47:28.680076'::timestamp,
                'member'
            )
            ON CONFLICT DO NOTHING
        """), {"admin_user_id": admin_user_id})

        conn.execute(text("""
            INSERT INTO user_clubs (user_id, club_id, join_date, role)
            VALUES (
                :admin_user_id,
                '681ff682-f876-40d0-bfda-994197a879e1'::uuid,
                '2025-11-23T03:46:28.316326'::timestamp,
                'member'
            )
            ON CONFLICT DO NOTHING
        """), {"admin_user_id": admin_user_id})


def downgrade() -> None:
    """
    Remove seeded data.

    Note: Downgrade is intentionally not implemented to preserve data safety.
    If you need to remove this data, do it manually.
    """
    pass
