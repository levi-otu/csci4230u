/**
 * CreateClubModal Component
 * Modal for creating a new club
 */

import React, { useState } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/global/components/ui/sheet';
import { Button } from '@/global/components/ui/button';
import { Input } from '@/global/components/ui/input';
import { Label } from '@/global/components/ui/label';
import type { CreateClubRequest } from '@/global/models/club.models';

export interface CreateClubModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (clubData: CreateClubRequest) => void;
  isCreating?: boolean;
}

/**
 * CreateClubModal component for creating new clubs
 */
export const CreateClubModal: React.FC<CreateClubModalProps> = ({
  open,
  onOpenChange,
  onSubmit,
  isCreating = false,
}) => {
  const [formData, setFormData] = useState<CreateClubRequest>({
    name: '',
    description: '',
    topic: '',
    max_members: undefined,
  });

  const [errors, setErrors] = useState<Partial<Record<keyof CreateClubRequest, string>>>({});

  // Handle input change
  const handleChange = (field: keyof CreateClubRequest, value: string | number) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value === '' ? undefined : value,
    }));
    // Clear error for this field
    setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  // Validate form
  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof CreateClubRequest, string>> = {};

    if (!formData.name || formData.name.trim() === '') {
      newErrors.name = 'Club name is required';
    } else if (formData.name.length > 255) {
      newErrors.name = 'Club name must be 255 characters or less';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    if (formData.topic && formData.topic.length > 255) {
      newErrors.topic = 'Topic must be 255 characters or less';
    }

    if (formData.max_members && formData.max_members <= 0) {
      newErrors.max_members = 'Max members must be greater than 0';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submit
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    // Submit the form
    onSubmit(formData);

    // Reset form
    setFormData({
      name: '',
      description: '',
      topic: '',
      max_members: undefined,
    });
    setErrors({});
  };

  // Handle modal close
  const handleClose = () => {
    if (!isCreating) {
      setFormData({
        name: '',
        description: '',
        topic: '',
        max_members: undefined,
      });
      setErrors({});
      onOpenChange(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={handleClose}>
      <SheetContent side="right" className="w-full sm:max-w-md overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Create New Club</SheetTitle>
          <SheetDescription>
            Fill in the details below to create a new book club. Members can join once it's created.
          </SheetDescription>
        </SheetHeader>

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          {/* Club Name */}
          <div className="space-y-2">
            <Label htmlFor="name">
              Club Name <span className="text-destructive">*</span>
            </Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., Mystery Book Club"
              disabled={isCreating}
            />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name}</p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <textarea
              id="description"
              value={formData.description || ''}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Describe what your club is about..."
              disabled={isCreating}
              className="flex min-h-[120px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 resize-none"
            />
            {errors.description && (
              <p className="text-sm text-destructive">{errors.description}</p>
            )}
          </div>

          {/* Topic */}
          <div className="space-y-2">
            <Label htmlFor="topic">Topic</Label>
            <Input
              id="topic"
              value={formData.topic || ''}
              onChange={(e) => handleChange('topic', e.target.value)}
              placeholder="e.g., Mystery, Fiction, Non-Fiction"
              disabled={isCreating}
            />
            {errors.topic && (
              <p className="text-sm text-destructive">{errors.topic}</p>
            )}
          </div>

          {/* Max Members */}
          <div className="space-y-2">
            <Label htmlFor="max_members">Max Members (Optional)</Label>
            <Input
              id="max_members"
              type="number"
              value={formData.max_members || ''}
              onChange={(e) =>
                handleChange('max_members', parseInt(e.target.value) || 0)
              }
              placeholder="Leave empty for unlimited"
              disabled={isCreating}
              min="1"
            />
            {errors.max_members && (
              <p className="text-sm text-destructive">{errors.max_members}</p>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isCreating}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isCreating} className="flex-1">
              {isCreating ? 'Creating...' : 'Create Club'}
            </Button>
          </div>
        </form>
      </SheetContent>
    </Sheet>
  );
};

export default CreateClubModal;
