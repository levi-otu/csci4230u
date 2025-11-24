/**
 * Library Page
 * Beautiful personal library with shelf-like display
 */

import React, { useEffect, useState, useMemo } from 'react';
import { Plus, BookOpen, Heart, Star, Search, Grid3x3, List } from 'lucide-react';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
import { useAppSelector } from '@/global/hooks/useAppSelector';
import {
  fetchMyLibraryAsync,
  fetchLibraryStatsAsync,
  setLibraryFilters,
} from '@/global/store/slices';
import { Button } from '@/global/components/ui/button';
import { Input } from '@/global/components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '@/global/components/ui/tabs';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/global/components/ui/select';
import { BookCard } from '../components/BookCard';
import { AddBookModal } from '../components/AddBookModal';
import { BookDetailModal } from '../components/BookDetailModal';
import { LibraryStats } from '../components/LibraryStats';
import type { UserBook } from '@/global/models/library.models';

/**
 * Library Page Component
 */
export const Library: React.FC = () => {
  const dispatch = useAppDispatch();
  const { myLibrary, libraryStats, isLoadingLibrary, libraryFilters } =
    useAppSelector((state) => state.library);

  const [isAddBookOpen, setIsAddBookOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState<UserBook | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filterTab, setFilterTab] = useState<'all' | 'reading' | 'finished' | 'favorites'>('all');

  // Fetch library and stats on mount
  useEffect(() => {
    dispatch(fetchMyLibraryAsync(libraryFilters));
    dispatch(fetchLibraryStatsAsync());
  }, [dispatch, libraryFilters]);

  // Get the current version of selectedBook from myLibrary
  // We need to find the book each time myLibrary changes to ensure we have the latest data
  const currentSelectedBook = useMemo(() => {
    if (!selectedBook) return null;
    const found = myLibrary.find((b) => b.id === selectedBook.id);
    if (found) {
      console.log('📚 Modal book updated - Status:', found.reading_status, 'Book object:', found);
    }
    return found || selectedBook;
  }, [myLibrary, selectedBook]);

  // Filter books based on search and tab
  const filteredBooks = myLibrary.filter((userBook) => {
    // Search filter
    const matchesSearch =
      searchQuery === '' ||
      userBook.book?.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      userBook.book?.author.toLowerCase().includes(searchQuery.toLowerCase());

    // Tab filter
    let matchesTab = true;
    switch (filterTab) {
      case 'reading':
        matchesTab = userBook.reading_status === 'reading';
        break;
      case 'finished':
        matchesTab = userBook.reading_status === 'finished';
        break;
      case 'favorites':
        matchesTab = userBook.is_favorite;
        break;
      default:
        matchesTab = true;
    }

    return matchesSearch && matchesTab;
  });

  // Handle filter changes
  const handleRatingFilter = (value: string) => {
    const minRating = value === 'all' ? null : parseFloat(value);
    dispatch(setLibraryFilters({ ...libraryFilters, min_rating: minRating }));
  };

  const handleBookClick = (book: UserBook) => {
    setSelectedBook(book);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 dark:from-zinc-900 dark:via-neutral-900 dark:to-stone-900">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl shadow-lg">
                <BookOpen className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
                  My Library
                </h1>
                <p className="text-muted-foreground mt-1">
                  Your personal collection of literary treasures
                </p>
              </div>
            </div>
            <Button
              onClick={() => setIsAddBookOpen(true)}
              size="lg"
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 shadow-lg"
            >
              <Plus className="h-5 w-5 mr-2" />
              Add Book
            </Button>
          </div>

          {/* Stats */}
          {libraryStats && <LibraryStats stats={libraryStats} />}
        </div>

        {/* Filters & Search */}
        <div className="mb-6 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by title or author..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-card border-border focus:border-amber-400"
              />
            </div>

            {/* Rating Filter */}
            <Select onValueChange={handleRatingFilter} defaultValue="all">
              <SelectTrigger className="w-48 bg-card border-border">
                <Star className="h-4 w-4 mr-2 text-amber-500" />
                <SelectValue placeholder="Filter by rating" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Ratings</SelectItem>
                <SelectItem value="4">4+ Stars</SelectItem>
                <SelectItem value="3">3+ Stars</SelectItem>
                <SelectItem value="2">2+ Stars</SelectItem>
                <SelectItem value="1">1+ Stars</SelectItem>
              </SelectContent>
            </Select>

            {/* View Mode */}
            <div className="flex gap-2 bg-card p-1 rounded-lg border border-border">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('grid')}
                className={viewMode === 'grid' ? 'bg-gradient-to-r from-amber-500 to-orange-600' : ''}
              >
                <Grid3x3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('list')}
                className={viewMode === 'list' ? 'bg-gradient-to-r from-amber-500 to-orange-600' : ''}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Tabs */}
          <Tabs value={filterTab} onValueChange={(v) => setFilterTab(v as any)} className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-card border-border">
              <TabsTrigger value="all" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-500 data-[state=active]:to-orange-600 data-[state=active]:text-white">
                All Books
                <span className="ml-2 px-2 py-0.5 text-xs bg-amber-100 dark:bg-amber-900 rounded-full">
                  {myLibrary.length}
                </span>
              </TabsTrigger>
              <TabsTrigger value="reading" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-500 data-[state=active]:to-orange-600 data-[state=active]:text-white">
                Currently Reading
                <span className="ml-2 px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900 rounded-full">
                  {myLibrary.filter((b) => b.reading_status === 'reading').length}
                </span>
              </TabsTrigger>
              <TabsTrigger value="finished" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-500 data-[state=active]:to-orange-600 data-[state=active]:text-white">
                Finished
                <span className="ml-2 px-2 py-0.5 text-xs bg-green-100 dark:bg-green-900 rounded-full">
                  {myLibrary.filter((b) => b.reading_status === 'finished').length}
                </span>
              </TabsTrigger>
              <TabsTrigger value="favorites" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-amber-500 data-[state=active]:to-orange-600 data-[state=active]:text-white">
                <Heart className="h-4 w-4 mr-1" />
                Favorites
                <span className="ml-2 px-2 py-0.5 text-xs bg-red-100 dark:bg-red-900 rounded-full">
                  {myLibrary.filter((b) => b.is_favorite).length}
                </span>
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Books Display */}
        {isLoadingLibrary ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center space-y-3">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto" />
              <p className="text-muted-foreground">Loading your library...</p>
            </div>
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="p-6 bg-amber-100 dark:bg-amber-900/20 rounded-full mb-6">
              <BookOpen className="h-16 w-16 text-amber-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-2">
              {searchQuery || filterTab !== 'all'
                ? 'No books found'
                : 'Your library is empty'}
            </h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              {searchQuery || filterTab !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Start building your personal collection by adding your first book'}
            </p>
            {!searchQuery && filterTab === 'all' && (
              <Button
                onClick={() => setIsAddBookOpen(true)}
                size="lg"
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
              >
                <Plus className="h-5 w-5 mr-2" />
                Add Your First Book
              </Button>
            )}
          </div>
        ) : (
          <div
            className={
              viewMode === 'grid'
                ? 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6'
                : 'space-y-4'
            }
          >
            {filteredBooks.map((userBook) => (
              <BookCard
                key={userBook.id}
                userBook={userBook}
                viewMode={viewMode}
                onClick={() => handleBookClick(userBook)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      <AddBookModal
        open={isAddBookOpen}
        onOpenChange={setIsAddBookOpen}
      />

      {currentSelectedBook && (
        <BookDetailModal
          userBook={currentSelectedBook}
          open={!!currentSelectedBook}
          onOpenChange={(open) => !open && setSelectedBook(null)}
        />
      )}
    </div>
  );
};

export default Library;
