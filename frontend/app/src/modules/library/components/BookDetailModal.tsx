/**
 * BookDetailModal Component
 * Modal for viewing and editing book details, ratings, reviews, and notes
 */

import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Heart,
  Star,
  Calendar,
  CheckCircle2,
  Trash2,
  Save,
  Edit,
  Loader2,
} from 'lucide-react';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
import { useAppSelector } from '@/global/hooks/useAppSelector';
import {
  updateUserBookAsync,
  setReadingStatusAsync,
  toggleFavoriteAsync,
  removeFromLibraryAsync,
} from '@/global/store/slices';
import { Button } from '@/global/components/ui/button';
import { Label } from '@/global/components/ui/label';
import { Textarea } from '@/global/components/ui/textarea';
import { Badge } from '@/global/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/global/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/global/components/ui/alert-dialog';
import type { UserBook } from '@/global/models/library.models';
import { EditBookModal } from './EditBookModal';

interface BookDetailModalProps {
  userBook: UserBook;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * BookDetailModal Component
 */
export const BookDetailModal: React.FC<BookDetailModalProps> = ({
  userBook,
  open,
  onOpenChange,
}) => {
  const dispatch = useAppDispatch();
  const { isLoading } = useAppSelector((state) => state.library);

  const [rating, setRating] = useState<number>(userBook.rating || 0);
  const [review, setReview] = useState(userBook.review || '');
  const [notes, setNotes] = useState(userBook.notes || '');
  const [hasChanges, setHasChanges] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [hoveredStar, setHoveredStar] = useState<number>(0);

  // Local state for immediate UI updates
  const [readingStatus, setReadingStatus] = useState<'unread' | 'reading' | 'finished'>(
    userBook.reading_status
  );
  const [isFavorite, setIsFavorite] = useState(userBook.is_favorite);
  const [readDate, setReadDate] = useState(userBook.read_date);
  const [isTogglingRead, setIsTogglingRead] = useState(false);
  const [isTogglingFavorite, setIsTogglingFavorite] = useState(false);

  const { book } = userBook;

  // Reset local state when userBook changes
  useEffect(() => {
    console.log('🔄 Modal useEffect triggered - Status:', userBook.reading_status);
    setRating(userBook.rating || 0);
    setReview(userBook.review || '');
    setNotes(userBook.notes || '');
    setReadingStatus(userBook.reading_status);
    setIsFavorite(userBook.is_favorite);
    setReadDate(userBook.read_date);
    setHasChanges(false);
  }, [userBook]);

  // Track changes
  useEffect(() => {
    const changed =
      rating !== (userBook.rating || 0) ||
      review !== (userBook.review || '') ||
      notes !== (userBook.notes || '');
    setHasChanges(changed);
  }, [rating, review, notes, userBook]);

  if (!book) return null;

  // Handle save changes
  const handleSave = async () => {
    const result = await dispatch(
      updateUserBookAsync({
        userBookId: userBook.id,
        data: {
          rating: rating > 0 ? rating : undefined,
          review: review.trim() || undefined,
          notes: notes.trim() || undefined,
        },
      })
    );

    if (updateUserBookAsync.fulfilled.match(result)) {
      setHasChanges(false);
    }
  };

  // Cycle reading status: unread → reading → finished → unread
  const handleToggleRead = async () => {
    setIsTogglingRead(true);
    try {
      let nextStatus: 'unread' | 'reading' | 'finished';

      if (readingStatus === 'unread') {
        nextStatus = 'reading';
      } else if (readingStatus === 'reading') {
        nextStatus = 'finished';
      } else {
        nextStatus = 'unread';
      }

      console.log('🎯 Changing status from', readingStatus, 'to', nextStatus);

      const result = await dispatch(
        setReadingStatusAsync({
          userBookId: userBook.id,
          reading_status: nextStatus,
        })
      );

      if (setReadingStatusAsync.fulfilled.match(result)) {
        console.log('✅ Status change succeeded, payload:', result.payload.reading_status);
        setReadingStatus(nextStatus);
        setReadDate(result.payload.read_date);
      } else {
        console.log('❌ Status change failed');
      }
    } finally {
      setIsTogglingRead(false);
    }
  };

  // Toggle favorite
  const handleToggleFavorite = async () => {
    setIsTogglingFavorite(true);
    try {
      const result = await dispatch(toggleFavoriteAsync(userBook.id));
      if (toggleFavoriteAsync.fulfilled.match(result)) {
        setIsFavorite(result.payload.is_favorite);
      }
    } finally {
      setIsTogglingFavorite(false);
    }
  };

  // Remove from library
  const handleRemove = async () => {
    const result = await dispatch(removeFromLibraryAsync(userBook.id));

    if (removeFromLibraryAsync.fulfilled.match(result)) {
      setShowDeleteDialog(false);
      onOpenChange(false);
    }
  };

  // Render star rating
  const renderStars = () => {
    return (
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((star) => {
          const isFilled = star <= (hoveredStar || rating);
          return (
            <button
              key={star}
              type="button"
              onClick={() => setRating(star)}
              onMouseEnter={() => setHoveredStar(star)}
              onMouseLeave={() => setHoveredStar(0)}
              className="focus:outline-none transition-transform hover:scale-110"
            >
              <Star
                className={`h-8 w-8 ${
                  isFilled
                    ? 'fill-amber-400 text-amber-400'
                    : 'text-gray-300 hover:text-amber-300'
                }`}
              />
            </button>
          );
        })}
        {rating > 0 && (
          <span className="ml-2 text-sm text-muted-foreground">
            {rating}.0 / 5.0
          </span>
        )}
      </div>
    );
  };

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <DialogTitle className="text-2xl bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
                  {book.title}
                </DialogTitle>
                {book.series_title && (
                  <p className="text-sm text-amber-600 dark:text-amber-400 mt-1">
                    {book.series_title} {book.volume_number && `- Volume ${book.volume_number}`}
                    {book.volume_title && `: ${book.volume_title}`}
                  </p>
                )}
                <DialogDescription>by {book.author}</DialogDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowEditModal(true)}
                className="flex-shrink-0 mt-1"
              >
                <Edit className="h-4 w-4 mr-2" />
                Edit
              </Button>
            </div>
          </DialogHeader>

          <div className="space-y-6">
            {/* Book Overview */}
            <div className="flex gap-6">
              {/* Book Cover */}
              <div className="w-40 aspect-[2/3] bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg overflow-hidden flex-shrink-0">
                {book.cover_image_url ? (
                  <img
                    src={book.cover_image_url}
                    alt={book.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <BookOpen className="h-16 w-16 text-amber-300" />
                  </div>
                )}
              </div>

              {/* Book Info */}
              <div className="flex-1 space-y-4">
                <div className="flex flex-wrap gap-2">
                  {book.genre && <Badge variant="outline">{book.genre}</Badge>}
                  {book.date_of_first_publish && (
                    <Badge variant="outline">
                      Published {new Date(book.date_of_first_publish).getFullYear()}
                    </Badge>
                  )}
                </div>

                {book.description && (
                  <div className="space-y-2">
                    <h3 className="font-semibold text-sm">Description</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {book.description}
                    </p>
                  </div>
                )}

                {/* Status Badges */}
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleToggleRead}
                    disabled={isLoading || isTogglingRead}
                    className={
                      readingStatus === 'finished'
                        ? 'border-green-500 text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-950/50'
                        : readingStatus === 'reading'
                        ? 'border-blue-500 text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/50'
                        : 'border-gray-500 text-gray-700 dark:text-gray-400 bg-gray-50 dark:bg-gray-950/50'
                    }
                  >
                    {isTogglingRead ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Updating...
                      </>
                    ) : readingStatus === 'finished' ? (
                      <>
                        <CheckCircle2 className="h-4 w-4 mr-2" />
                        Finished
                      </>
                    ) : readingStatus === 'reading' ? (
                      <>
                        <BookOpen className="h-4 w-4 mr-2" />
                        Currently Reading
                      </>
                    ) : (
                      <>
                        <BookOpen className="h-4 w-4 mr-2 opacity-50" />
                        Unread
                      </>
                    )}
                  </Button>

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleToggleFavorite}
                    disabled={isLoading || isTogglingFavorite}
                    className={
                      isFavorite
                        ? 'border-red-500 text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-950/50'
                        : ''
                    }
                  >
                    {isTogglingFavorite ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        {isFavorite ? 'Removing...' : 'Adding...'}
                      </>
                    ) : (
                      <>
                        <Heart
                          className={`h-4 w-4 mr-2 ${isFavorite ? 'fill-red-500 dark:fill-red-400' : ''}`}
                        />
                        {isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
                      </>
                    )}
                  </Button>
                </div>

                {/* Read Date */}
                {readingStatus === 'finished' && readDate && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    <span>
                      Read on {new Date(readDate).toLocaleDateString()}
                    </span>
                  </div>
                )}

                {/* Added Date */}
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>
                    Added on {new Date(userBook.added_date).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>

            {/* Rating Section */}
            <div className="space-y-3">
              <Label>Your Rating</Label>
              {renderStars()}
            </div>

            {/* Review Section */}
            <div className="space-y-2">
              <Label htmlFor="review">Your Review</Label>
              <Textarea
                id="review"
                placeholder="Share your thoughts about this book..."
                value={review}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setReview(e.target.value)}
                rows={5}
                className="border-amber-200 focus:border-amber-400 resize-none"
              />
            </div>

            {/* Notes Section */}
            <div className="space-y-2">
              <Label htmlFor="notes">Personal Notes</Label>
              <Textarea
                id="notes"
                placeholder="Add private notes or quotes..."
                value={notes}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setNotes(e.target.value)}
                rows={4}
                className="border-amber-200 focus:border-amber-400 resize-none"
              />
            </div>
          </div>

          <DialogFooter className="flex justify-between items-center">
            <Button
              variant="destructive"
              onClick={() => setShowDeleteDialog(true)}
              disabled={isLoading}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Remove from Library
            </Button>

            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => onOpenChange(false)}
                disabled={isLoading}
              >
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                disabled={!hasChanges || isLoading}
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
              >
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Remove from Library?</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to remove "{book.title}" from your library? This
              action cannot be undone and will delete all your notes, ratings, and
              reviews for this book.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleRemove}
              className="bg-red-600 hover:bg-red-700"
            >
              Remove Book
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Edit Book Modal */}
      <EditBookModal
        userBook={userBook}
        open={showEditModal}
        onOpenChange={setShowEditModal}
      />
    </>
  );
};

export default BookDetailModal;
