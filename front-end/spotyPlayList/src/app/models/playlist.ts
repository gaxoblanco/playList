export interface PlaylistDate {
  playlists: Playlist;
  bandInfo: BandInfo;
}

export interface Playlist {
  band_id: string;
  name: string;
  href: string;
  img: string[];
}

export interface BandInfo {
  failed_bands: string[];
  top_add: number;
  top_failed: number;
}
