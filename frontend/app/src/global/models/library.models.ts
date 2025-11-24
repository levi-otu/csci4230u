/**
 * Library models matching backend API schemas
 * For user's personal book library and reading lists
 */

/**
 * Book model from global catalog
 */
export interface Book {
  id: string;
  title: string;
  author: string;
  date_of_first_publish: string | null;
  genre: string | null;
  description: string | null;
  cover_image_url: string | null;
  // Multi-volume series support
  series_title: string | null;
  volume_number: number | null;
  volume_title: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Request payload for creating a book
 */
export interface CreateBookRequest {
  title: string;
  author: string;
  date_of_first_publish?: string | null;
  genre?: string | null;
  description?: string | null;
  cover_image_url?: string | null;
  // Multi-volume series support
  series_title?: string | null;
  volume_number?: number | null;
  volume_title?: string | null;
}

/**
 * Request payload for updating a book
 */
export interface UpdateBookRequest {
  title?: string;
  author?: string;
  date_of_first_publish?: string | null;
  genre?: string | null;
  description?: string | null;
  cover_image_url?: string | null;
  // Multi-volume series support
  series_title?: string | null;
  volume_number?: number | null;
  volume_title?: string | null;
}

/**
 * ISBN lookup request
 */
export interface ISBNLookupRequest {
  isbn: string;
}

/**
 * ISBN lookup response from external API
 */
export interface ISBNLookupResponse {
  found: boolean;
  title?: string | null;
  author?: string | null;
  publisher?: string | null;
  publish_date?: string | null;
  genre?: string | null;
  isbn_10?: string | null;
  isbn_13?: string | null;
  cover_url?: string | null;
  description?: string | null;
  page_count?: number | null;
  // Multi-volume series support
  series_title?: string | null;
  volume_number?: number | null;
  volume_title?: string | null;
  total_volumes?: number | null;
}

/**
 * User's book in their personal library
 */
export interface UserBook {
  id: string;
  user_id: string;
  book_id: string;
  book_version_id: string | null;
  added_date: string;
  is_read: boolean;
  read_date: string | null;
  reading_status: 'unread' | 'reading' | 'finished';
  rating: number | null; // 0.0 to 5.0
  review: string | null;
  notes: string | null;
  is_favorite: boolean;
  // Nested book data
  book?: Book;
}

/**
 * Request payload for adding book to library
 */
export interface AddToLibraryRequest {
  book_id: string;
  book_version_id?: string | null;
  is_read?: boolean;
  read_date?: string | null;
  rating?: number | null;
  review?: string | null;
  notes?: string | null;
  is_favorite?: boolean;
}

/**
 * Request payload for updating user book
 */
export interface UpdateUserBookRequest {
  is_read?: boolean;
  read_date?: string | null;
  reading_status?: 'unread' | 'reading' | 'finished';
  rating?: number | null;
  review?: string | null;
  notes?: string | null;
  is_favorite?: boolean;
}

/**
 * Quick action requests
 */
export interface MarkAsReadRequest {
  read_date?: string | null;
}

export interface AddRatingRequest {
  rating: number; // 0.0 to 5.0
}

export interface AddReviewRequest {
  review: string;
}

export interface AddNotesRequest {
  notes: string;
}

/**
 * Reading list
 */
export interface ReadingList {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  created_date: string;
  is_default: boolean;
  item_count: number;
}

/**
 * Request payload for creating reading list
 */
export interface CreateReadingListRequest {
  name: string;
  description?: string | null;
  is_default?: boolean;
}

/**
 * Request payload for updating reading list
 */
export interface UpdateReadingListRequest {
  name?: string;
  description?: string | null;
}

/**
 * Reading list item (book in a reading list)
 */
export interface ReadingListItem {
  id: string;
  reading_list_id: string;
  user_book_id: string;
  order_index: number;
  added_date: string;
  // Nested user book data
  user_book?: UserBook;
}

/**
 * Reading list with all its items
 */
export interface ReadingListWithItems extends ReadingList {
  items: ReadingListItem[];
}

/**
 * Request payload for adding book to reading list
 */
export interface AddToReadingListRequest {
  user_book_id: string;
  order_index?: number | null;
}

/**
 * Request payload for reordering reading list items
 */
export interface ReorderItemsRequest {
  items: Array<[string, number]>; // Array of [item_id, new_order_index]
}

/**
 * Library statistics
 */
export interface LibraryStats {
  total_books: number;
  read_books: number;
  unread_books: number;
  favorite_books: number;
  total_reading_lists: number;
  average_rating: number | null;
  books_read_this_year: number;
  books_read_this_month: number;
}

/**
 * Library filters for querying
 */
export interface LibraryFilters {
  skip?: number;
  limit?: number;
  is_read?: boolean | null;
  is_favorite?: boolean | null;
  min_rating?: number | null;
}
