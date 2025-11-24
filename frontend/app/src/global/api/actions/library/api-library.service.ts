/**
 * Library API service
 * Handles all library-related API calls
 */

import { httpClient } from '@/global/api/http-client';
import type {
  AddNotesRequest,
  AddRatingRequest,
  AddReviewRequest,
  AddToLibraryRequest,
  AddToReadingListRequest,
  Book,
  CreateBookRequest,
  CreateReadingListRequest,
  ISBNLookupRequest,
  ISBNLookupResponse,
  LibraryFilters,
  LibraryStats,
  MarkAsReadRequest,
  ReadingList,
  ReadingListWithItems,
  ReorderItemsRequest,
  UpdateBookRequest,
  UpdateReadingListRequest,
  UpdateUserBookRequest,
  UserBook,
} from '@/global/models/library.models';

/**
 * Library service for managing books and user library
 */
export class LibraryService {
  private static readonly BASE_ENDPOINT = '/api/library';

  // Book Catalog Operations

  /**
   * Create a new book in the global catalog
   */
  static async createBook(data: CreateBookRequest): Promise<Book> {
    return await httpClient.post<Book>(`${this.BASE_ENDPOINT}/books`, data);
  }

  /**
   * Get all books from the catalog
   */
  static async getBooks(skip: number = 0, limit: number = 100): Promise<Book[]> {
    return await httpClient.get<Book[]>(
      `${this.BASE_ENDPOINT}/books?skip=${skip}&limit=${limit}`
    );
  }

  /**
   * Get a specific book by ID
   */
  static async getBook(bookId: string): Promise<Book> {
    return await httpClient.get<Book>(`${this.BASE_ENDPOINT}/books/${bookId}`);
  }

  /**
   * Update a book in the catalog
   */
  static async updateBook(bookId: string, data: UpdateBookRequest): Promise<Book> {
    return await httpClient.put<Book>(`${this.BASE_ENDPOINT}/books/${bookId}`, data);
  }

  /**
   * Delete a book from the catalog
   */
  static async deleteBook(bookId: string): Promise<void> {
    await httpClient.delete(`${this.BASE_ENDPOINT}/books/${bookId}`);
  }

  // ISBN Lookup

  /**
   * Look up book information by ISBN
   */
  static async lookupISBN(isbn: string): Promise<ISBNLookupResponse> {
    const request: ISBNLookupRequest = { isbn };
    return await httpClient.post<ISBNLookupResponse>(
      `${this.BASE_ENDPOINT}/books/lookup/isbn`,
      request
    );
  }

  // User Library Operations

  /**
   * Add a book to user's library
   */
  static async addToLibrary(data: AddToLibraryRequest): Promise<UserBook> {
    return await httpClient.post<UserBook>(`${this.BASE_ENDPOINT}/my-library`, data);
  }

  /**
   * Get user's library with optional filters
   */
  static async getMyLibrary(filters?: LibraryFilters): Promise<UserBook[]> {
    const params = new URLSearchParams();
    if (filters?.skip !== undefined) params.append('skip', filters.skip.toString());
    if (filters?.limit !== undefined) params.append('limit', filters.limit.toString());
    if (filters?.is_read !== undefined && filters.is_read !== null) {
      params.append('is_read', filters.is_read.toString());
    }
    if (filters?.is_favorite !== undefined && filters.is_favorite !== null) {
      params.append('is_favorite', filters.is_favorite.toString());
    }
    if (filters?.min_rating !== undefined && filters.min_rating !== null) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_ENDPOINT}/my-library?${queryString}`
      : `${this.BASE_ENDPOINT}/my-library`;

    return await httpClient.get<UserBook[]>(url);
  }

  /**
   * Get a specific book from user's library
   */
  static async getLibraryBook(userBookId: string): Promise<UserBook> {
    return await httpClient.get<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}`
    );
  }

  /**
   * Update a book in user's library
   */
  static async updateLibraryBook(
    userBookId: string,
    data: UpdateUserBookRequest
  ): Promise<UserBook> {
    return await httpClient.put<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}`,
      data
    );
  }

  /**
   * Remove a book from user's library
   */
  static async removeFromLibrary(userBookId: string): Promise<void> {
    await httpClient.delete(`${this.BASE_ENDPOINT}/my-library/${userBookId}`);
  }

  // Quick Actions

  /**
   * Mark a book as read
   */
  static async markAsRead(
    userBookId: string,
    data?: MarkAsReadRequest
  ): Promise<UserBook> {
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/mark-read`,
      data || {}
    );
  }

  /**
   * Mark a book as unread
   */
  static async markAsUnread(userBookId: string): Promise<UserBook> {
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/mark-unread`,
      {}
    );
  }

  /**
   * Set reading status for a book
   */
  static async setReadingStatus(
    userBookId: string,
    reading_status: 'unread' | 'reading' | 'finished'
  ): Promise<UserBook> {
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/reading-status`,
      { reading_status }
    );
  }

  /**
   * Add or update rating for a book
   */
  static async addRating(
    userBookId: string,
    rating: number
  ): Promise<UserBook> {
    const data: AddRatingRequest = { rating };
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/rating`,
      data
    );
  }

  /**
   * Add or update review for a book
   */
  static async addReview(
    userBookId: string,
    review: string
  ): Promise<UserBook> {
    const data: AddReviewRequest = { review };
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/review`,
      data
    );
  }

  /**
   * Add or update notes for a book
   */
  static async addNotes(
    userBookId: string,
    notes: string
  ): Promise<UserBook> {
    const data: AddNotesRequest = { notes };
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/notes`,
      data
    );
  }

  /**
   * Toggle favorite status for a book
   */
  static async toggleFavorite(userBookId: string): Promise<UserBook> {
    return await httpClient.post<UserBook>(
      `${this.BASE_ENDPOINT}/my-library/${userBookId}/toggle-favorite`,
      {}
    );
  }

  // Reading Lists

  /**
   * Create a new reading list
   */
  static async createReadingList(
    data: CreateReadingListRequest
  ): Promise<ReadingList> {
    return await httpClient.post<ReadingList>(
      `${this.BASE_ENDPOINT}/reading-lists`,
      data
    );
  }

  /**
   * Get all reading lists for the current user
   */
  static async getReadingLists(): Promise<ReadingList[]> {
    return await httpClient.get<ReadingList[]>(
      `${this.BASE_ENDPOINT}/reading-lists`
    );
  }

  /**
   * Get a reading list with all its items
   */
  static async getReadingList(readingListId: string): Promise<ReadingListWithItems> {
    return await httpClient.get<ReadingListWithItems>(
      `${this.BASE_ENDPOINT}/reading-lists/${readingListId}`
    );
  }

  /**
   * Update a reading list
   */
  static async updateReadingList(
    readingListId: string,
    data: UpdateReadingListRequest
  ): Promise<ReadingList> {
    return await httpClient.put<ReadingList>(
      `${this.BASE_ENDPOINT}/reading-lists/${readingListId}`,
      data
    );
  }

  /**
   * Delete a reading list
   */
  static async deleteReadingList(readingListId: string): Promise<void> {
    await httpClient.delete(`${this.BASE_ENDPOINT}/reading-lists/${readingListId}`);
  }

  /**
   * Add a book to a reading list
   */
  static async addToReadingList(
    readingListId: string,
    data: AddToReadingListRequest
  ): Promise<void> {
    await httpClient.post(
      `${this.BASE_ENDPOINT}/reading-lists/${readingListId}/items`,
      data
    );
  }

  /**
   * Remove a book from a reading list
   */
  static async removeFromReadingList(
    readingListId: string,
    userBookId: string
  ): Promise<void> {
    await httpClient.delete(
      `${this.BASE_ENDPOINT}/reading-lists/${readingListId}/items/${userBookId}`
    );
  }

  /**
   * Reorder items in a reading list
   */
  static async reorderReadingList(
    readingListId: string,
    data: ReorderItemsRequest
  ): Promise<void> {
    await httpClient.post(
      `${this.BASE_ENDPOINT}/reading-lists/${readingListId}/reorder`,
      data
    );
  }

  // Statistics

  /**
   * Get library statistics for the current user
   */
  static async getLibraryStats(): Promise<LibraryStats> {
    return await httpClient.get<LibraryStats>(`${this.BASE_ENDPOINT}/stats`);
  }
}

export default LibraryService;
