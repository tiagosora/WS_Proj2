import csv
from collections import defaultdict, Counter
from wikidata import (
    get_album_description,
    get_album_image,
    get_album_release_date,
    get_album_genres,
    get_artist_description,
    get_artist_image,
    get_artist_work_period_start,
    get_artist_work_period_end,
    get_artist_genres 
)

# Define namespaces
namespace = "http://webify.ws/ontology#"
foaf_namespace = "http://xmlns.com/foaf/0.1/"

# Function to convert milliseconds to xsd:duration
def ms_to_duration(ms):
    seconds = (ms / 1000) % 60
    minutes = (ms / (1000 * 60)) % 60
    return f"PT{int(minutes)}M{round(seconds, 3)}S"

# Function to escape special characters in HTML attributes
def escape_attribute(value):
    if value is None:
        return ""
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# Function to initialize the RDFa content
def initialize_rdfa():
    return [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Webify RDFa</title>',
        '</head>',
        '<body>',
        '    <div xmlns="http://www.w3.org/1999/xhtml"',
        '         xmlns:foaf="http://xmlns.com/foaf/0.1/"',
        '         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"',
        '         xmlns:owl="http://www.w3.org/2002/07/owl#"',
        '         xmlns:xsd="http://www.w3.org/2001/XMLSchema#"',
        '         xmlns:sp="http://spinrdf.org/sp#"',
        '         xmlns:webify="http://webify.ws/ontology#">',
        '        <div typeof="owl:Ontology">',
        '            <span property="rdfs:comment" lang="en">Webify Ontology for music tracks, albums, artists, and genres.</span>',
        '            <span property="rdfs:label" lang="en">Webify Ontology</span>',
        '            <span property="owl:versionInfo">1.0</span>',
        '        </div>'
    ]

# Function to process track data and add to RDFa
def process_tracks(csv_file, rdfa, album_artists, max_tracks):
    added_albums, added_artists, added_discs, added_genres = set(), set(), set(), set()
    processed_rows = 0

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if processed_rows >= max_tracks:
                break

            processed_rows += 1
            track_uri = f"{namespace}{row['id']}"
            track_name = escape_attribute(row['name'])
            rdfa.append(f'<div typeof="webify:MusicTrack" about="{track_uri}">')
            rdfa.append(f'    <span property="webify:hasID">{row["id"]}</span>')
            rdfa.append(f'    <span property="webify:hasName">{track_name}</span>')
            rdfa.append(f'    <span property="rdfs:label">{track_name}</span>')
            rdfa.append(f'    <span property="webify:hasTrackNumber">{int(row["track_number"])}</span>')
            rdfa.append(f'    <span property="webify:isExplicit">{row["explicit"] == "True"}</span>')
            rdfa.append(f'    <span property="webify:hasDanceability">{float(row["danceability"])}</span>')
            rdfa.append(f'    <span property="webify:hasEnergy">{float(row["energy"])}</span>')
            rdfa.append(f'    <span property="webify:hasKey">{int(row["key"])}</span>')
            rdfa.append(f'    <span property="webify:hasLoudness">{float(row["loudness"])}</span>')
            rdfa.append(f'    <span property="webify:hasMode">{int(row["mode"])}</span>')
            rdfa.append(f'    <span property="webify:hasSpeechiness">{float(row["speechiness"])}</span>')
            rdfa.append(f'    <span property="webify:hasAcousticness">{float(row["acousticness"])}</span>')
            rdfa.append(f'    <span property="webify:hasInstrumentalness">{float(row["instrumentalness"])}</span>')
            rdfa.append(f'    <span property="webify:hasLiveness">{float(row["liveness"])}</span>')
            rdfa.append(f'    <span property="webify:hasValence">{float(row["valence"])}</span>')
            rdfa.append(f'    <span property="webify:hasTempo">{float(row["tempo"])}</span>')
            rdfa.append(f'    <span property="webify:hasDuration">{ms_to_duration(int(row["duration_ms"]))}</span>')
            rdfa.append(f'    <span property="webify:hasTimeSignature">{int(float(row["time_signature"]))}</span>')
            rdfa.append(f'    <span property="webify:hasReleaseDate">{row["release_date"]}</span>')
            rdfa.append(f'    <span property="webify:hasYear">{int(row["year"])}</span>')

            # Process related album, disc, and artist data
            process_album(row, rdfa, album_artists, added_albums, added_genres)
            process_disc(row, rdfa, added_discs)
            process_artists(row, rdfa, added_artists, added_genres)
            
            rdfa.append('</div>')

            # Output progress with percentage
            progress = (processed_rows / max_tracks) * 100
            if processed_rows % 100 == 0 or processed_rows == max_tracks:
                print(f"Processed {processed_rows} of {max_tracks} rows ({progress:.2f}%).")

# Function to process album data and add to RDFa
def process_album(row, rdfa, album_artists, added_albums, added_genres):
    album_id = row['album_id']
    album_uri = f"{namespace}{album_id}"
    album_name = escape_attribute(row['album'])
    if album_id not in added_albums:
        rdfa.append(f'<div typeof="webify:Album" about="{album_uri}">')
        rdfa.append(f'    <span property="webify:hasID">{album_id}</span>')
        rdfa.append(f'    <span property="webify:hasName">{album_name}</span>')

        # Add album details
        album_description = escape_attribute(get_album_description(album_id))
        album_image = get_album_image(album_id)
        album_release_date = get_album_release_date(album_id)

        if album_description:
            rdfa.append(f'    <span property="webify:hasDescription">{album_description}</span>')
        if album_image:
            rdfa.append(f'    <span property="foaf:depiction" resource="{album_image}"></span>')
        if album_release_date:
            rdfa.append(f'    <span property="webify:hasAlbumReleaseDate">{album_release_date}</span>')

        rdfa.append(f'    <span property="rdfs:label">{album_name}</span>')

        # Determine the most frequent artist for the album
        most_frequent_artist_id = Counter(album_artists[album_id]).most_common(1)[0][0]
        most_frequent_artist_uri = f"{namespace}{most_frequent_artist_id}"
        rdfa.append(f'    <span rel="webify:isCreatedByArtist" resource="{most_frequent_artist_uri}"></span>')

        added_albums.add(album_id)

        # Add genres for the album
        album_genres_dict = get_album_genres(album_id)
        album_genres = album_genres_dict.get(album_id, [])
        for genre in album_genres:
            genre_id = genre['id']
            genre_uri = f"{namespace}{genre_id}"
            if genre_id not in added_genres:
                genre_label = escape_attribute(genre['label'])
                genre_description = escape_attribute(genre['description'])
                rdfa.append(f'<div typeof="webify:Genre" about="{genre_uri}">')
                rdfa.append(f'    <span property="webify:hasID">{genre_id}</span>')
                rdfa.append(f'    <span property="rdfs:label">{genre_label}</span>')
                rdfa.append(f'    <span property="webify:hasDescription">{genre_description}</span>')
                rdfa.append('</div>')
                added_genres.add(genre_id)
            rdfa.append(f'    <span rel="webify:hasGenre" resource="{genre_uri}"></span>')

        rdfa.append('</div>')

# Function to process disc data and add to RDFa
def process_disc(row, rdfa, added_discs):
    album_id = row['album_id']
    album_name = escape_attribute(row['album'])
    disc_uri = f"{namespace}{album_id}_Disc{row['disc_number']}"
    disc_label = f"{album_name} - Disc {int(row['disc_number'])}"
    if disc_uri not in added_discs:
        rdfa.append(f'<div typeof="webify:Disc" about="{disc_uri}">')
        rdfa.append(f'    <span property="webify:hasID">{album_id}_Disc{row["disc_number"]}</span>')
        rdfa.append(f'    <span property="webify:hasDiscNumber">{int(row["disc_number"])}</span>')
        rdfa.append(f'    <span rel="webify:isPartOfAlbum" resource="{namespace}{album_id}"></span>')
        rdfa.append(f'    <span property="rdfs:label">{disc_label}</span>')
        rdfa.append('</div>')
        added_discs.add(disc_uri)

    # Link track to disc
    rdfa.append(f'    <span rel="webify:isPartOfDisc" resource="{disc_uri}"></span>')

# Function to process artist data and add to RDFa
def process_artists(row, rdfa, added_artists, added_genres):
    artist_ids = eval(row['artist_ids'])  # Assuming this field is a list in string format
    artists = eval(row['artists'])  # Assuming this field is a list in string format
    for artist_id, artist_name in zip(artist_ids, artists):
        artist_uri = f"{namespace}{artist_id}"
        artist_name = escape_attribute(artist_name)
        if artist_id not in added_artists:
            rdfa.append(f'<div typeof="webify:Artist" about="{artist_uri}">')
            rdfa.append(f'    <span property="webify:hasID">{artist_id}</span>')
            rdfa.append(f'    <span property="webify:hasName">{artist_name}</span>')

            # Add artist details
            artist_description = escape_attribute(get_artist_description(artist_id))
            artist_image = get_artist_image(artist_id)
            artist_work_period_start = get_artist_work_period_start(artist_id)
            artist_work_period_end = get_artist_work_period_end(artist_id)

            if artist_description:
                rdfa.append(f'    <span property="webify:hasDescription">{artist_description}</span>')
            if artist_image:
                rdfa.append(f'    <span property="foaf:depiction" resource="{artist_image}"></span>')
            if artist_work_period_start:
                rdfa.append(f'    <span property="webify:hasArtistWorkPeriodStart">{artist_work_period_start}</span>')
            if artist_work_period_end:
                rdfa.append(f'    <span property="webify:hasArtistWorkPeriodEnd">{artist_work_period_end}</span>')

            rdfa.append(f'    <span property="rdfs:label">{artist_name}</span>')

            # Add genres for the artist
            artist_genres_dict = get_artist_genres(artist_id)
            artist_genres = artist_genres_dict.get(artist_id, [])
            for genre in artist_genres:
                genre_id = genre['id']
                genre_uri = f"{namespace}{genre_id}"
                if genre_id not in added_genres:
                    genre_label = escape_attribute(genre['label'])
                    genre_description = escape_attribute(genre['description'])
                    rdfa.append(f'<div typeof="webify:Genre" about="{genre_uri}">')
                    rdfa.append(f'    <span property="webify:hasID">{genre_id}</span>')
                    rdfa.append(f'    <span property="rdfs:label">{genre_label}</span>')
                    rdfa.append(f'    <span property="webify:hasDescription">{genre_description}</span>')
                    rdfa.append('</div>')
                    added_genres.add(genre_id)
                rdfa.append(f'    <span rel="webify:hasGenre" resource="{genre_uri}"></span>')

            rdfa.append('</div>')
            added_artists.add(artist_id)

        rdfa.append(f'    <span rel="webify:isCreatedByArtist" resource="{artist_uri}"></span>')

# Function to gather artist data for each album
def gather_artist_data(csv_file):
    album_artists = defaultdict(list)
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            album_id = row['album_id']
            artist_ids = eval(row['artist_ids'])
            for artist_id in artist_ids:
                album_artists[album_id].append(artist_id)
    return album_artists

# Main function to generate RDFa content
def generate_rdfa(csv_file, max_tracks):
    rdfa = initialize_rdfa()
    process_tracks(csv_file, rdfa, gather_artist_data(csv_file), max_tracks)
    rdfa.append('</div>')
    rdfa.append('</body>')
    rdfa.append('</html>')
    return rdfa

# Write RDFa to file
def write_rdfa_to_file(rdfa, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rdfa))

def main():
    csv_file = 'tracks_features.csv'
    max_tracks = 1  # Example limit for the number of tracks to process
    output_file = 'webify_rdfa.html'

    rdfa = generate_rdfa(csv_file, max_tracks)
    write_rdfa_to_file(rdfa, output_file)
    print(f"RDFa content written to {output_file}")

if __name__ == "__main__":
    main()
