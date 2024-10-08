export interface ListBand {
  band_id: string;
  name: string;
  top_tracks?: top_track[];
  href?: string;
  img?: string;
  genres?: string[];
}

interface top_track {
  name: string;
  url: string;
}
