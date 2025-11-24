/**
 * EditBookModal Component
 * Modal for editing book metadata and user-specific data
 */

import React, { useState, useEffect } from 'react';
import { BookOpen, Calendar, Save, Loader2 } from 'lucide-react';
import { useAppDispatch } from '@/global/hooks/useAppDispatch';
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
  DialogFooter,
} from '@/global/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/global/components/ui/alert-dialog';
import type { UserBook } from '@/global/models/library.models';
import { updateBookAsync, updateUserBookAsync } from '@/global/store/slices';

interface EditBookModalProps {
  userBook: UserBook;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * EditBookModal Component
 */
export const EditBookModal: React.FC<EditBookModalProps> = ({
  userBook,
  open,
  onOpenChange,
}) => {
  const dispatch = useAppDispatch();

  const { book, is_read, read_date } = userBook;

  // Form state for book metadata
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [genre, setGenre] = useState('');
  const [description, setDescription] = useState('');
  const [coverImageUrl, setCoverImageUrl] = useState('');
  const [dateOfFirstPublish, setDateOfFirstPublish] = useState('');
  // Multi-volume series fields
  const [seriesTitle, setSeriesTitle] = useState('');
  const [volumeNumber, setVolumeNumber] = useState('');
  const [volumeTitle, setVolumeTitle] = useState('');

  // Form state for user-specific data
  const [readDateValue, setReadDateValue] = useState('');

  // UI state
  const [hasChanges, setHasChanges] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [errorDialogOpen, setErrorDialogOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Initialize form when userBook changes
  useEffect(() => {
    if (book) {
      setTitle(book.title || '');
      setAuthor(book.author || '');
      setGenre(book.genre || '');
      setDescription(book.description || '');
      setCoverImageUrl(book.cover_image_url || '');
      setDateOfFirstPublish(
        book.date_of_first_publish
          ? new Date(book.date_of_first_publish).toISOString().split('T')[0]
          : ''
      );
      setSeriesTitle(book.series_title || '');
      setVolumeNumber(book.volume_number?.toString() || '');
      setVolumeTitle(book.volume_title || '');
    }

    setReadDateValue(
      read_date ? new Date(read_date).toISOString().split('T')[0] : ''
    );
    setHasChanges(false);
  }, [book, read_date, open]);

  // Track changes
  useEffect(() => {
    if (!book) return;

    const bookChanged =
      title !== (book.title || '') ||
      author !== (book.author || '') ||
      genre !== (book.genre || '') ||
      description !== (book.description || '') ||
      coverImageUrl !== (book.cover_image_url || '') ||
      dateOfFirstPublish !==
        (book.date_of_first_publish
          ? new Date(book.date_of_first_publish).toISOString().split('T')[0]
          : '') ||
      seriesTitle !== (book.series_title || '') ||
      volumeNumber !== (book.volume_number?.toString() || '') ||
      volumeTitle !== (book.volume_title || '');

    const readDateChanged =
      is_read &&
      readDateValue !==
        (read_date ? new Date(read_date).toISOString().split('T')[0] : '');

    setHasChanges(bookChanged || readDateChanged);
  }, [
    title,
    author,
    genre,
    description,
    coverImageUrl,
    dateOfFirstPublish,
    seriesTitle,
    volumeNumber,
    volumeTitle,
    readDateValue,
    book,
    is_read,
    read_date,
  ]);

  if (!book) return null;

  /**
   * Handle save changes
   */
  const handleSave = async () => {
    setIsSaving(true);

    try {
      // Step 1: Update book metadata if changed
      const bookChanged =
        title !== (book.title || '') ||
        author !== (book.author || '') ||
        genre !== (book.genre || '') ||
        description !== (book.description || '') ||
        coverImageUrl !== (book.cover_image_url || '') ||
        dateOfFirstPublish !==
          (book.date_of_first_publish
            ? new Date(book.date_of_first_publish).toISOString().split('T')[0]
            : '') ||
        seriesTitle !== (book.series_title || '') ||
        volumeNumber !== (book.volume_number?.toString() || '') ||
        volumeTitle !== (book.volume_title || '');

      if (bookChanged) {
        // Convert year-only date to full date format
        let publicationDate = dateOfFirstPublish.trim();
        if (publicationDate && /^\d{4}$/.test(publicationDate)) {
          publicationDate = `${publicationDate}-01-01`;
        }

        const updateBookResult = await dispatch(
          updateBookAsync({
            bookId: book.id,
            data: {
              title: title.trim(),
              author: author.trim(),
              genre: genre.trim() || null,
              description: description.trim() || null,
              cover_image_url: coverImageUrl.trim() || null,
              date_of_first_publish: publicationDate || null,
              series_title: seriesTitle.trim() || null,
              volume_number: volumeNumber ? parseInt(volumeNumber, 10) : null,
              volume_title: volumeTitle.trim() || null,
            },
          })
        );

        if (updateBookAsync.rejected.match(updateBookResult)) {
          const error = updateBookResult.payload || 'Failed to update book metadata';
          setErrorMessage(typeof error === 'string' ? error : JSON.stringify(error));
          setErrorDialogOpen(true);
          setIsSaving(false);
          return;
        }
      }

      // Step 2: Update read date if changed and book is marked as read
      const readDateChanged =
        is_read &&
        readDateValue !==
          (read_date ? new Date(read_date).toISOString().split('T')[0] : '');

      if (readDateChanged && readDateValue) {
        const updateUserBookResult = await dispatch(
          updateUserBookAsync({
            userBookId: userBook.id,
            data: {
              read_date: readDateValue,
            },
          })
        );

        if (updateUserBookAsync.rejected.match(updateUserBookResult)) {
          const error = updateUserBookResult.payload || 'Failed to update read date';
          setErrorMessage(typeof error === 'string' ? error : JSON.stringify(error));
          setErrorDialogOpen(true);
          setIsSaving(false);
          return;
        }
      }

      // Success - close modal
      setIsSaving(false);
      setHasChanges(false);
      onOpenChange(false);
    } catch (error: any) {
      setErrorMessage(error?.message || 'An unexpected error occurred');
      setErrorDialogOpen(true);
      setIsSaving(false);
    }
  };

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-2xl flex items-center gap-2">
              <BookOpen className="h-6 w-6 text-amber-600" />
              Edit Book Details
            </DialogTitle>
            <DialogDescription>
              Update book metadata and reading information
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            {/* Title */}
            <div className="space-y-2">
              <Label htmlFor="title">
                Title <span className="text-red-500">*</span>
              </Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Book title"
                className="bg-card"
              />
            </div>

            {/* Author */}
            <div className="space-y-2">
              <Label htmlFor="author">
                Author <span className="text-red-500">*</span>
              </Label>
              <Input
                id="author"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                placeholder="Author name"
                className="bg-card"
              />
            </div>

            {/* Genre */}
            <div className="space-y-2">
              <Label htmlFor="genre">Genre</Label>
              <Input
                id="genre"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                placeholder="e.g., Fiction, Mystery, Science Fiction"
                className="bg-card"
              />
            </div>

            {/* Publication Date */}
            <div className="space-y-2">
              <Label htmlFor="publish-date">Publication Date</Label>
              <Input
                id="publish-date"
                type="date"
                value={dateOfFirstPublish}
                onChange={(e) => setDateOfFirstPublish(e.target.value)}
                className="bg-card"
              />
              <p className="text-xs text-muted-foreground">
                You can also enter just a year (e.g., 2003)
              </p>
            </div>

            {/* Multi-volume Series Section */}
            <div className="border-t border-border pt-4 space-y-4">
              <h4 className="text-sm font-medium text-amber-600 dark:text-amber-400">
                Multi-Volume Series (Optional)
              </h4>

              {/* Series Title */}
              <div className="space-y-2">
                <Label htmlFor="series-title">Series Title</Label>
                <Input
                  id="series-title"
                  value={seriesTitle}
                  onChange={(e) => setSeriesTitle(e.target.value)}
                  placeholder="e.g., Reformed Dogmatics"
                  className="bg-card"
                />
              </div>

              {/* Volume Number and Title in a grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="volume-number">Volume Number</Label>
                  <Input
                    id="volume-number"
                    type="number"
                    value={volumeNumber}
                    onChange={(e) => setVolumeNumber(e.target.value)}
                    placeholder="e.g., 2"
                    className="bg-card"
                    min="1"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="volume-title">Volume Title</Label>
                  <Input
                    id="volume-title"
                    value={volumeTitle}
                    onChange={(e) => setVolumeTitle(e.target.value)}
                    placeholder="e.g., God and creation"
                    className="bg-card"
                  />
                </div>
              </div>

              <p className="text-xs text-muted-foreground">
                Leave these fields empty to remove volume information
              </p>
            </div>

            {/* Cover Image URL */}
            <div className="space-y-2">
              <Label htmlFor="cover-url">Cover Image URL</Label>
              <Input
                id="cover-url"
                type="url"
                value={coverImageUrl}
                onChange={(e) => setCoverImageUrl(e.target.value)}
                placeholder="https://example.com/cover.jpg"
                className="bg-card"
              />
              {coverImageUrl && (
                <div className="mt-2 flex justify-center">
                  <div className="w-32 aspect-[2/3] bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg overflow-hidden">
                    <img
                      src={coverImageUrl}
                      alt="Cover preview"
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                      }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Book description or summary..."
                rows={5}
                className="bg-card resize-none"
              />
            </div>

            {/* Read Date (only if book is marked as read) */}
            {is_read && (
              <div className="space-y-2 pt-4 border-t border-border">
                <Label htmlFor="read-date" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Date Read
                </Label>
                <Input
                  id="read-date"
                  type="date"
                  value={readDateValue}
                  onChange={(e) => setReadDateValue(e.target.value)}
                  className="bg-card"
                />
              </div>
            )}
          </div>

          <DialogFooter className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isSaving}
            >
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              disabled={!hasChanges || isSaving || !title.trim() || !author.trim()}
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700"
            >
              {isSaving ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Save Changes
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Error Dialog */}
      <AlertDialog open={errorDialogOpen} onOpenChange={setErrorDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Error Updating Book</AlertDialogTitle>
            <AlertDialogDescription>{errorMessage}</AlertDialogDescription>
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

export default EditBookModal;
