/**
 * AddBookModal Component
 * Modal for adding books to library with ISBN lookup or manual entry
 */

import React, { useState } from 'react';
import { Search, BookOpen, Plus, Loader2, AlertCircle } from 'lucide-react';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
import { useAppSelector } from '@/global/hooks/useAppSelector';
import { lookupISBNAsync, clearISBNLookup, createBookAsync, addToLibraryAsync } from '@/global/store/slices';
import { Button } from '@/global/components/ui/button';
import { Input } from '@/global/components/ui/input';
import { Label } from '@/global/components/ui/label';
import { Textarea } from '@/global/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/global/components/ui/dialog';
import { Alert, AlertDescription } from '@/global/components/ui/alert';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/global/components/ui/alert-dialog';

interface AddBookModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * AddBookModal Component
 */
export const AddBookModal: React.FC<AddBookModalProps> = ({ open, onOpenChange }) => {
  const dispatch = useAppDispatch();
  const { isbnLookupResult, isLoading, isLookingUpISBN, isAddingToLibrary, error } = useAppSelector((state) => state.library);

  const [isbn, setIsbn] = useState('');
  const [showManualEntry, setShowManualEntry] = useState(false);
  const [errorDialogOpen, setErrorDialogOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Manual entry form state
  const [manualData, setManualData] = useState({
    title: '',
    author: '',
    genre: '',
    description: '',
    date_of_first_publish: '',
    cover_image_url: '',
    series_title: '',
    volume_number: '',
    volume_title: '',
  });

  // Handle ISBN lookup
  const handleISBNLookup = async () => {
    if (!isbn.trim()) return;

    const result = await dispatch(lookupISBNAsync(isbn.trim()));

    if (lookupISBNAsync.fulfilled.match(result)) {
      // ISBN lookup successful
      if (!result.payload.found) {
        // Book not found, show manual entry
        setShowManualEntry(true);
      }
    }
  };

  // Handle adding book from ISBN lookup
  const handleAddFromISBN = async () => {
    if (!isbnLookupResult || !isbnLookupResult.found) return;

    // Pre-fill manual form with ISBN data and show it
    setManualData({
      title: isbnLookupResult.title || '',
      author: isbnLookupResult.author || '',
      genre: isbnLookupResult.genre || '',
      description: isbnLookupResult.description || '',
      date_of_first_publish: isbnLookupResult.publish_date || '',
      cover_image_url: isbnLookupResult.cover_url || '',
      series_title: isbnLookupResult.series_title || '',
      volume_number: isbnLookupResult.volume_number?.toString() || '',
      volume_title: isbnLookupResult.volume_title || '',
    });
    setShowManualEntry(true);
  };

  // Handle manual book entry
  const handleManualSubmit = async () => {
    if (!manualData.title.trim() || !manualData.author.trim()) return;

    // Convert publication date to proper format if it's just a year
    let publicationDate = manualData.date_of_first_publish?.trim();
    if (publicationDate) {
      // If it's just a year (e.g., "2003"), convert to ISO date format (e.g., "2003-01-01")
      if (/^\d{4}$/.test(publicationDate)) {
        publicationDate = `${publicationDate}-01-01`;
      }
    }

    // Step 1: Create the book in the global catalog
    const createResult = await dispatch(
      createBookAsync({
        title: manualData.title.trim(),
        author: manualData.author.trim(),
        genre: manualData.genre.trim() || undefined,
        description: manualData.description.trim() || undefined,
        date_of_first_publish: publicationDate || undefined,
        cover_image_url: manualData.cover_image_url.trim() || undefined,
        series_title: manualData.series_title.trim() || undefined,
        volume_number: manualData.volume_number ? parseInt(manualData.volume_number, 10) : undefined,
        volume_title: manualData.volume_title.trim() || undefined,
      })
    );

    // Handle book creation failure
    if (createBookAsync.rejected.match(createResult)) {
      const error = createResult.payload || 'Failed to create book. Please try again.';
      // If error is an object, stringify it
      const errorMsg = typeof error === 'string' ? error : JSON.stringify(error, null, 2);
      setErrorMessage(errorMsg);
      setErrorDialogOpen(true);
      return;
    }

    // Step 2: If book creation succeeded, add it to user's library
    if (createBookAsync.fulfilled.match(createResult)) {
      const book = createResult.payload;
      const addResult = await dispatch(
        addToLibraryAsync({
          book_id: book.id,
        })
      );

      // Handle adding to library failure
      if (addToLibraryAsync.rejected.match(addResult)) {
        const error = addResult.payload || 'Failed to add book to library. Please try again.';
        const errorMsg = typeof error === 'string' ? error : JSON.stringify(error, null, 2);
        setErrorMessage(errorMsg);
        setErrorDialogOpen(true);
        return;
      }

      // Close modal if successfully added to library
      if (addToLibraryAsync.fulfilled.match(addResult)) {
        handleClose();
      }
    }
  };

  // Reset and close modal
  const handleClose = () => {
    setIsbn('');
    setShowManualEntry(false);
    setManualData({
      title: '',
      author: '',
      genre: '',
      description: '',
      date_of_first_publish: '',
      cover_image_url: '',
      series_title: '',
      volume_number: '',
      volume_title: '',
    });
    dispatch(clearISBNLookup());
    onOpenChange(false);
  };

  // Render ISBN lookup result
  const renderISBNResult = () => {
    if (!isbnLookupResult) return null;

    if (!isbnLookupResult.found) {
      return (
        <Alert className="border-amber-600/50 bg-amber-950/50 dark:bg-amber-950/30">
          <AlertCircle className="h-4 w-4 text-amber-500" />
          <AlertDescription className="text-amber-200 dark:text-amber-300">
            Book not found. You can add it manually below.
          </AlertDescription>
        </Alert>
      );
    }

    return (
      <div className="space-y-4">
        <Alert className="border-green-600/50 bg-green-950/50 dark:bg-green-950/30">
          <AlertCircle className="h-4 w-4 text-green-500" />
          <AlertDescription className="text-green-200 dark:text-green-300">
            Book found! Review the details below.
          </AlertDescription>
        </Alert>

        <div className="flex gap-4 p-4 bg-card rounded-lg border border-border">
          {/* Book Cover */}
          <div className="w-24 aspect-[2/3] bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg overflow-hidden flex-shrink-0">
            {isbnLookupResult.cover_url ? (
              <img
                src={isbnLookupResult.cover_url}
                alt={isbnLookupResult.title || 'Book cover'}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <BookOpen className="h-8 w-8 text-amber-300" />
              </div>
            )}
          </div>

          {/* Book Details */}
          <div className="flex-1 space-y-2">
            <h3 className="font-semibold text-lg">{isbnLookupResult.title}</h3>
            {isbnLookupResult.series_title && (
              <p className="text-sm text-amber-600 dark:text-amber-400">
                <span className="font-medium">Series:</span> {isbnLookupResult.series_title}
                {isbnLookupResult.volume_number && ` - Volume ${isbnLookupResult.volume_number}`}
                {isbnLookupResult.total_volumes && ` of ${isbnLookupResult.total_volumes}`}
              </p>
            )}
            {isbnLookupResult.volume_title && (
              <p className="text-sm text-amber-600 dark:text-amber-400">
                <span className="font-medium">Volume Title:</span> {isbnLookupResult.volume_title}
              </p>
            )}
            <p className="text-sm text-muted-foreground">by {isbnLookupResult.author}</p>
            {isbnLookupResult.publisher && (
              <p className="text-sm">
                <span className="font-medium">Publisher:</span> {isbnLookupResult.publisher}
              </p>
            )}
            {isbnLookupResult.publish_date && (
              <p className="text-sm">
                <span className="font-medium">Published:</span> {isbnLookupResult.publish_date}
              </p>
            )}
            {(isbnLookupResult.isbn_10 || isbnLookupResult.isbn_13) && (
              <p className="text-sm">
                <span className="font-medium">ISBN:</span> {isbnLookupResult.isbn_13 || isbnLookupResult.isbn_10}
              </p>
            )}
            {isbnLookupResult.description && (
              <p className="text-sm text-muted-foreground line-clamp-3 mt-2">
                {isbnLookupResult.description}
              </p>
            )}
          </div>
        </div>

        <Button
          onClick={handleAddFromISBN}
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          Continue with This Book
        </Button>
      </div>
    );
  };

  // Render manual entry form
  const renderManualEntry = () => (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">
          Title <span className="text-red-500">*</span>
        </Label>
        <Input
          id="title"
          placeholder="Enter book title"
          value={manualData.title}
          onChange={(e) => setManualData({ ...manualData, title: e.target.value })}
          className=""
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="author">
          Author <span className="text-red-500">*</span>
        </Label>
        <Input
          id="author"
          placeholder="Enter author name"
          value={manualData.author}
          onChange={(e) => setManualData({ ...manualData, author: e.target.value })}
          className=""
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="genre">Genre</Label>
        <Input
          id="genre"
          placeholder="e.g., Fiction, Mystery, Science Fiction"
          value={manualData.genre}
          onChange={(e) => setManualData({ ...manualData, genre: e.target.value })}
          className=""
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="date">Publication Date</Label>
        <Input
          id="date"
          type="text"
          placeholder="e.g., 2003 or 2003-01-15"
          value={manualData.date_of_first_publish}
          onChange={(e) =>
            setManualData({ ...manualData, date_of_first_publish: e.target.value })
          }
          className=""
        />
      </div>

      {/* Multi-volume Series Fields */}
      <div className="border-t border-border pt-4 space-y-4">
        <h4 className="text-sm font-medium text-amber-600 dark:text-amber-400">Multi-Volume Series (Optional)</h4>

        <div className="space-y-2">
          <Label htmlFor="series_title">Series Title</Label>
          <Input
            id="series_title"
            placeholder="e.g., Reformed Dogmatics"
            value={manualData.series_title}
            onChange={(e) => setManualData({ ...manualData, series_title: e.target.value })}
            className=""
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="volume_number">Volume Number</Label>
            <Input
              id="volume_number"
              type="number"
              placeholder="e.g., 2"
              value={manualData.volume_number}
              onChange={(e) => setManualData({ ...manualData, volume_number: e.target.value })}
              className=""
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="volume_title">Volume Title</Label>
            <Input
              id="volume_title"
              placeholder="e.g., God and creation"
              value={manualData.volume_title}
              onChange={(e) => setManualData({ ...manualData, volume_title: e.target.value })}
              className=""
            />
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="cover">Cover Image URL</Label>
        <Input
          id="cover"
          placeholder="https://example.com/cover.jpg"
          value={manualData.cover_image_url}
          onChange={(e) =>
            setManualData({ ...manualData, cover_image_url: e.target.value })
          }
          className=""
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          placeholder="Enter a brief description of the book"
          value={manualData.description}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setManualData({ ...manualData, description: e.target.value })}
          rows={4}
          className="resize-none"
        />
      </div>

      <Button
        onClick={handleManualSubmit}
        disabled={!manualData.title.trim() || !manualData.author.trim() || isAddingToLibrary || isLoading}
        className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
      >
        {(isAddingToLibrary || isLoading) ? (
          <>
            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            Adding to Library...
          </>
        ) : (
          <>
            <Plus className="h-4 w-4 mr-2" />
            Add to My Library
          </>
        )}
      </Button>
    </div>
  );

  return (
    <>
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
            Add Book to Library
          </DialogTitle>
          <DialogDescription>
            Search by ISBN or add a book manually
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* ISBN Lookup Section */}
          {!showManualEntry && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="isbn">ISBN Number</Label>
                <div className="flex gap-2">
                  <Input
                    id="isbn"
                    placeholder="Enter ISBN (e.g., 9780743273565)"
                    value={isbn}
                    onChange={(e) => setIsbn(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleISBNLookup()}
                    className="flex-1"
                  />
                  <Button
                    onClick={handleISBNLookup}
                    disabled={!isbn.trim() || isLookingUpISBN}
                    className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
                  >
                    {isLookingUpISBN ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Search className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>

              {renderISBNResult()}

              {/* Manual Entry Toggle */}
              {(!isbnLookupResult || !isbnLookupResult.found) && (
                <div className="text-center">
                  <Button
                    variant="outline"
                    onClick={() => setShowManualEntry(true)}
                    className="border-amber-600 text-amber-500 hover:bg-amber-950/50"
                  >
                    {isbnLookupResult && !isbnLookupResult.found
                      ? 'Add Book Manually'
                      : 'Or Add Manually'}
                  </Button>
                </div>
              )}
            </div>
          )}

          {/* Manual Entry Form */}
          {showManualEntry && (
            <div className="space-y-4">
              {!isbnLookupResult && (
                <Button
                  variant="ghost"
                  onClick={() => setShowManualEntry(false)}
                  className="text-amber-500 hover:bg-amber-950/50"
                >
                  ← Back to ISBN Lookup
                </Button>
              )}
              {renderManualEntry()}
            </div>
          )}

          {/* Error Display */}
          {error && (
            <Alert className="border-red-600/50 bg-red-950/50 dark:bg-red-950/30">
              <AlertCircle className="h-4 w-4 text-red-500" />
              <AlertDescription className="text-red-200 dark:text-red-300">{error}</AlertDescription>
            </Alert>
          )}
        </div>
      </DialogContent>
    </Dialog>

    {/* Error Dialog */}
    <AlertDialog open={errorDialogOpen} onOpenChange={setErrorDialogOpen}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Error Adding Book</AlertDialogTitle>
          <AlertDialogDescription>
            {errorMessage}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogAction onClick={() => setErrorDialogOpen(false)}>
            OK
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
    </>
  );
};

export default AddBookModal;
