/**
 * Library Redux Slice
 * Manages library state using Redux Toolkit
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import LibraryService from '@/global/api/actions/library/api-library.service';
import type {
  AddToLibraryRequest,
  AddToReadingListRequest,
  Book,
  CreateBookRequest,
  CreateReadingListRequest,
  ISBNLookupResponse,
  LibraryFilters,
  LibraryStats,
  ReadingList,
  ReadingListWithItems,
  UpdateBookRequest,
  UpdateUserBookRequest,
  UserBook,
} from '@/global/models/library.models';

/**
 * Library state interface
 */
export interface LibraryState {
  // Books catalog
  books: Book[];
  selectedBook: Book | null;

  // User library
  myLibrary: UserBook[];
  selectedUserBook: UserBook | null;
  libraryFilters: LibraryFilters;

  // Reading lists
  readingLists: ReadingList[];
  selectedReadingList: ReadingListWithItems | null;

  // ISBN lookup
  isbnLookupResult: ISBNLookupResponse | null;

  // Statistics
  libraryStats: LibraryStats | null;

  // Loading states
  isLoading: boolean;
  isLoadingLibrary: boolean;
  isLoadingReadingLists: boolean;
  isAddingToLibrary: boolean;
  isCreatingReadingList: boolean;
  isLookingUpISBN: boolean;

  // Error state
  error: string | null;
}

/**
 * Initial library state
 */
const initialState: LibraryState = {
  books: [],
  selectedBook: null,
  myLibrary: [],
  selectedUserBook: null,
  libraryFilters: {
    skip: 0,
    limit: 100,
  },
  readingLists: [],
  selectedReadingList: null,
  isbnLookupResult: null,
  libraryStats: null,
  isLoading: false,
  isLoadingLibrary: false,
  isLoadingReadingLists: false,
  isAddingToLibrary: false,
  isCreatingReadingList: false,
  isLookingUpISBN: false,
  error: null,
};

// Async Thunks

/**
 * Fetch all books from catalog
 */
export const fetchBooksAsync = createAsyncThunk<
  Book[],
  { skip?: number; limit?: number },
  { rejectValue: string }
>(
  'library/fetchBooks',
  async ({ skip = 0, limit = 100 }, { rejectWithValue }) => {
    try {
      return await LibraryService.getBooks(skip, limit);
    } catch (error: any) {
      return rejectWithValue(
        error?.data?.detail || error?.message || 'Failed to fetch books'
      );
    }
  }
);

/**
 * Create a new book
 */
export const createBookAsync = createAsyncThunk<
  Book,
  CreateBookRequest,
  { rejectValue: string }
>('library/createBook', async (data, { rejectWithValue }) => {
  try {
    return await LibraryService.createBook(data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to create book'
    );
  }
});

/**
 * Update a book
 */
export const updateBookAsync = createAsyncThunk<
  Book,
  { bookId: string; data: UpdateBookRequest },
  { rejectValue: string }
>('library/updateBook', async ({ bookId, data }, { rejectWithValue }) => {
  try {
    return await LibraryService.updateBook(bookId, data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to update book'
    );
  }
});

/**
 * Look up book by ISBN
 */
export const lookupISBNAsync = createAsyncThunk<
  ISBNLookupResponse,
  string,
  { rejectValue: string }
>('library/lookupISBN', async (isbn, { rejectWithValue }) => {
  try {
    return await LibraryService.lookupISBN(isbn);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to lookup ISBN'
    );
  }
});

/**
 * Fetch user's library
 */
export const fetchMyLibraryAsync = createAsyncThunk<
  UserBook[],
  LibraryFilters | undefined,
  { rejectValue: string }
>('library/fetchMyLibrary', async (filters, { rejectWithValue }) => {
  try {
    return await LibraryService.getMyLibrary(filters);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to fetch library'
    );
  }
});

/**
 * Add book to library
 */
export const addToLibraryAsync = createAsyncThunk<
  UserBook,
  AddToLibraryRequest,
  { rejectValue: string }
>('library/addToLibrary', async (data, { rejectWithValue }) => {
  try {
    return await LibraryService.addToLibrary(data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to add book to library'
    );
  }
});

/**
 * Update user book
 */
export const updateUserBookAsync = createAsyncThunk<
  UserBook,
  { userBookId: string; data: UpdateUserBookRequest },
  { rejectValue: string }
>('library/updateUserBook', async ({ userBookId, data }, { rejectWithValue }) => {
  try {
    return await LibraryService.updateLibraryBook(userBookId, data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to update book'
    );
  }
});

/**
 * Remove book from library
 */
export const removeFromLibraryAsync = createAsyncThunk<
  string,
  string,
  { rejectValue: string }
>('library/removeFromLibrary', async (userBookId, { rejectWithValue }) => {
  try {
    await LibraryService.removeFromLibrary(userBookId);
    return userBookId;
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to remove book'
    );
  }
});

/**
 * Mark book as read
 */
export const markAsReadAsync = createAsyncThunk<
  UserBook,
  string,
  { rejectValue: string }
>('library/markAsRead', async (userBookId, { rejectWithValue }) => {
  try {
    return await LibraryService.markAsRead(userBookId);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to mark as read'
    );
  }
});

/**
 * Mark book as unread
 */
export const markAsUnreadAsync = createAsyncThunk<
  UserBook,
  string,
  { rejectValue: string }
>('library/markAsUnread', async (userBookId, { rejectWithValue }) => {
  try {
    return await LibraryService.markAsUnread(userBookId);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to mark as unread'
    );
  }
});

/**
 * Set reading status
 */
export const setReadingStatusAsync = createAsyncThunk<
  UserBook,
  { userBookId: string; reading_status: 'unread' | 'reading' | 'finished' },
  { rejectValue: string }
>('library/setReadingStatus', async ({ userBookId, reading_status }, { rejectWithValue }) => {
  try {
    return await LibraryService.setReadingStatus(userBookId, reading_status);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to set reading status'
    );
  }
});

/**
 * Toggle favorite
 */
export const toggleFavoriteAsync = createAsyncThunk<
  UserBook,
  string,
  { rejectValue: string }
>('library/toggleFavorite', async (userBookId, { rejectWithValue }) => {
  try {
    return await LibraryService.toggleFavorite(userBookId);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to toggle favorite'
    );
  }
});

/**
 * Fetch reading lists
 */
export const fetchReadingListsAsync = createAsyncThunk<
  ReadingList[],
  void,
  { rejectValue: string }
>('library/fetchReadingLists', async (_, { rejectWithValue }) => {
  try {
    return await LibraryService.getReadingLists();
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to fetch reading lists'
    );
  }
});

/**
 * Fetch specific reading list with items
 */
export const fetchReadingListAsync = createAsyncThunk<
  ReadingListWithItems,
  string,
  { rejectValue: string }
>('library/fetchReadingList', async (readingListId, { rejectWithValue }) => {
  try {
    return await LibraryService.getReadingList(readingListId);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to fetch reading list'
    );
  }
});

/**
 * Create reading list
 */
export const createReadingListAsync = createAsyncThunk<
  ReadingList,
  CreateReadingListRequest,
  { rejectValue: string }
>('library/createReadingList', async (data, { rejectWithValue }) => {
  try {
    return await LibraryService.createReadingList(data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to create reading list'
    );
  }
});

/**
 * Add book to reading list
 */
export const addToReadingListAsync = createAsyncThunk<
  void,
  { readingListId: string; data: AddToReadingListRequest },
  { rejectValue: string }
>('library/addToReadingList', async ({ readingListId, data }, { rejectWithValue }) => {
  try {
    await LibraryService.addToReadingList(readingListId, data);
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to add to reading list'
    );
  }
});

/**
 * Fetch library statistics
 */
export const fetchLibraryStatsAsync = createAsyncThunk<
  LibraryStats,
  void,
  { rejectValue: string }
>('library/fetchStats', async (_, { rejectWithValue }) => {
  try {
    return await LibraryService.getLibraryStats();
  } catch (error: any) {
    return rejectWithValue(
      error?.data?.detail || error?.message || 'Failed to fetch statistics'
    );
  }
});

/**
 * Library slice
 */
const librarySlice = createSlice({
  name: 'library',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedBook: (state, action: PayloadAction<Book | null>) => {
      state.selectedBook = action.payload;
    },
    setSelectedUserBook: (state, action: PayloadAction<UserBook | null>) => {
      state.selectedUserBook = action.payload;
    },
    setLibraryFilters: (state, action: PayloadAction<LibraryFilters>) => {
      state.libraryFilters = action.payload;
    },
    clearISBNLookup: (state) => {
      state.isbnLookupResult = null;
    },
    resetLibraryState: () => initialState,
  },
  extraReducers: (builder) => {
    // Fetch books
    builder
      .addCase(fetchBooksAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchBooksAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.books = action.payload;
      })
      .addCase(fetchBooksAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch books';
      });

    // Create book
    builder
      .addCase(createBookAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createBookAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.books.unshift(action.payload);
      })
      .addCase(createBookAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to create book';
      });

    // Update book
    builder
      .addCase(updateBookAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateBookAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.books.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          state.books[index] = action.payload;
        }
        // Also update the book reference in myLibrary
        state.myLibrary = state.myLibrary.map((userBook) =>
          userBook.book?.id === action.payload.id
            ? { ...userBook, book: action.payload }
            : userBook
        );
      })
      .addCase(updateBookAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to update book';
      });

    // ISBN Lookup
    builder
      .addCase(lookupISBNAsync.pending, (state) => {
        state.isLookingUpISBN = true;
        state.isbnLookupResult = null;
        state.error = null;
      })
      .addCase(lookupISBNAsync.fulfilled, (state, action) => {
        state.isLookingUpISBN = false;
        state.isbnLookupResult = action.payload;
      })
      .addCase(lookupISBNAsync.rejected, (state, action) => {
        state.isLookingUpISBN = false;
        state.error = action.payload || 'Failed to lookup ISBN';
      });

    // Fetch library
    builder
      .addCase(fetchMyLibraryAsync.pending, (state) => {
        state.isLoadingLibrary = true;
        state.error = null;
      })
      .addCase(fetchMyLibraryAsync.fulfilled, (state, action) => {
        state.isLoadingLibrary = false;
        state.myLibrary = action.payload;
      })
      .addCase(fetchMyLibraryAsync.rejected, (state, action) => {
        state.isLoadingLibrary = false;
        state.error = action.payload || 'Failed to fetch library';
      });

    // Add to library
    builder
      .addCase(addToLibraryAsync.pending, (state) => {
        state.isAddingToLibrary = true;
        state.error = null;
      })
      .addCase(addToLibraryAsync.fulfilled, (state, action) => {
        state.isAddingToLibrary = false;
        state.myLibrary.unshift(action.payload);
      })
      .addCase(addToLibraryAsync.rejected, (state, action) => {
        state.isAddingToLibrary = false;
        state.error = action.payload || 'Failed to add to library';
      });

    // Update user book
    builder
      .addCase(updateUserBookAsync.fulfilled, (state, action) => {
        const index = state.myLibrary.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          // Create a new array with the updated book to ensure React detects the change
          state.myLibrary = [
            ...state.myLibrary.slice(0, index),
            action.payload,
            ...state.myLibrary.slice(index + 1)
          ];
        }
        if (state.selectedUserBook?.id === action.payload.id) {
          state.selectedUserBook = action.payload;
        }
      });

    // Remove from library
    builder
      .addCase(removeFromLibraryAsync.fulfilled, (state, action) => {
        state.myLibrary = state.myLibrary.filter((b) => b.id !== action.payload);
        if (state.selectedUserBook?.id === action.payload) {
          state.selectedUserBook = null;
        }
      });

    // Mark as read
    builder
      .addCase(markAsReadAsync.fulfilled, (state, action) => {
        const index = state.myLibrary.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          state.myLibrary[index] = action.payload;
        }
        if (state.selectedUserBook?.id === action.payload.id) {
          state.selectedUserBook = action.payload;
        }
      });

    // Mark as unread
    builder
      .addCase(markAsUnreadAsync.fulfilled, (state, action) => {
        const index = state.myLibrary.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          // Create a new array with the updated book to ensure React detects the change
          state.myLibrary = [
            ...state.myLibrary.slice(0, index),
            action.payload,
            ...state.myLibrary.slice(index + 1)
          ];
        }
        if (state.selectedUserBook?.id === action.payload.id) {
          state.selectedUserBook = action.payload;
        }
      });

    // Set reading status
    builder
      .addCase(setReadingStatusAsync.fulfilled, (state, action) => {
        const index = state.myLibrary.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          // Create a new array with the updated book to ensure React detects the change
          state.myLibrary = [
            ...state.myLibrary.slice(0, index),
            action.payload,
            ...state.myLibrary.slice(index + 1)
          ];
        }
        if (state.selectedUserBook?.id === action.payload.id) {
          state.selectedUserBook = action.payload;
        }
      });

    // Toggle favorite
    builder
      .addCase(toggleFavoriteAsync.fulfilled, (state, action) => {
        const index = state.myLibrary.findIndex((b) => b.id === action.payload.id);
        if (index !== -1) {
          // Create a new array with the updated book to ensure React detects the change
          state.myLibrary = [
            ...state.myLibrary.slice(0, index),
            action.payload,
            ...state.myLibrary.slice(index + 1)
          ];
        }
      });

    // Fetch reading lists
    builder
      .addCase(fetchReadingListsAsync.pending, (state) => {
        state.isLoadingReadingLists = true;
        state.error = null;
      })
      .addCase(fetchReadingListsAsync.fulfilled, (state, action) => {
        state.isLoadingReadingLists = false;
        state.readingLists = action.payload;
      })
      .addCase(fetchReadingListsAsync.rejected, (state, action) => {
        state.isLoadingReadingLists = false;
        state.error = action.payload || 'Failed to fetch reading lists';
      });

    // Fetch specific reading list
    builder
      .addCase(fetchReadingListAsync.fulfilled, (state, action) => {
        state.selectedReadingList = action.payload;
      });

    // Create reading list
    builder
      .addCase(createReadingListAsync.pending, (state) => {
        state.isCreatingReadingList = true;
        state.error = null;
      })
      .addCase(createReadingListAsync.fulfilled, (state, action) => {
        state.isCreatingReadingList = false;
        state.readingLists.unshift(action.payload);
      })
      .addCase(createReadingListAsync.rejected, (state, action) => {
        state.isCreatingReadingList = false;
        state.error = action.payload || 'Failed to create reading list';
      });

    // Fetch statistics
    builder
      .addCase(fetchLibraryStatsAsync.fulfilled, (state, action) => {
        state.libraryStats = action.payload;
      });
  },
});

/**
 * Export actions
 */
export const {
  clearError,
  setSelectedBook,
  setSelectedUserBook,
  setLibraryFilters,
  clearISBNLookup,
  resetLibraryState,
} = librarySlice.actions;

/**
 * Export reducer
 */
export default librarySlice.reducer;
