'use client';

import { useCallback, useState } from 'react';
import { Upload, FileText, X, CheckCircle, Sparkles, TrendingUp } from 'lucide-react';
import { useProfile } from '@/hooks/useProfile';
import { ALLOWED_RESUME_TYPES, MAX_RESUME_SIZE } from '@/lib/constants';
import { cn } from '@/lib/utils';

export default function ResumeUpload() {
  const { profile, uploadResume, isUploading } = useProfile();
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>('');
  const [uploadResult, setUploadResult] = useState<{
    success: boolean;
    data?: {
      error?: string;
      skillsAdded?: string[];
      skillsAlreadyExist?: string[];
      totalSkillsExtracted?: number;
      newSkillsAdded?: number;
    };
  } | null>(null);

  const validateFile = (file: File): boolean => {
    setError('');

    if (!ALLOWED_RESUME_TYPES.includes(file.type as typeof ALLOWED_RESUME_TYPES[number])) {
      setError('Please upload a PDF, DOCX, or TXT file');
      return false;
    }

    if (file.size > MAX_RESUME_SIZE) {
      setError('File size must be less than 10MB');
      return false;
    }

    return true;
  };

  const handleFile = (file: File) => {
    if (validateFile(file)) {
      setSelectedFile(file);
      setUploadResult(null);
    }
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      try {
        const result = await uploadResume(selectedFile);
        setUploadResult(result);
        setSelectedFile(null);
      } catch (error) {
        console.error('Upload failed:', error);
      }
    }
  };

  // Check if resume is uploaded
  const hasResume = profile?.resumeS3Uri || profile?.resumeUploadedAt;

  return (
    <div className="space-y-4">
      {/* Resume Status */}
      {hasResume && !uploadResult && (
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <div className="flex items-start gap-3">
            <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-green-900">Resume Uploaded</p>
              <p className="mt-1 text-xs text-green-700">
                {profile?.resumeUploadedAt && 
                  `Uploaded on ${new Date(profile.resumeUploadedAt).toLocaleDateString('en-IN', { 
                    day: 'numeric', 
                    month: 'short', 
                    year: 'numeric' 
                  })}`
                }
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Upload Result - Show what happened */}
      {uploadResult && (
        <div className={cn(
          "rounded-lg border p-4 space-y-3",
          uploadResult.data?.error 
            ? "border-yellow-200 bg-yellow-50"
            : "border-blue-200 bg-gradient-to-br from-blue-50 to-cyan-50"
        )}>
          <div className="flex items-start gap-3">
            {uploadResult.data?.error ? (
              <FileText className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            ) : (
              <Sparkles className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            )}
            <div className="flex-1 min-w-0">
              {uploadResult.data?.error ? (
                <>
                  <p className="text-sm font-bold text-yellow-900">Resume Uploaded</p>
                  <p className="mt-1 text-xs text-yellow-700">
                    {uploadResult.data.error}
                  </p>
                  <p className="mt-2 text-xs text-yellow-600">
                    Tip: For best results, use TXT or PDF format
                  </p>
                </>
              ) : (
                <>
                  <p className="text-sm font-bold text-blue-900">Resume Analyzed Successfully!</p>
                  <p className="mt-1 text-xs text-blue-700">
                    We extracted {uploadResult.data?.totalSkillsExtracted || 0} skills from your resume
                  </p>
                </>
              )}
            </div>
          </div>

          {/* Skills Added */}
          {!uploadResult.data?.error && (uploadResult.data?.newSkillsAdded ?? 0) > 0 && (
            <div className="rounded-lg bg-white/80 p-3 border border-blue-100">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <p className="text-xs font-semibold text-gray-900">
                  {uploadResult.data?.newSkillsAdded} New Skills Added
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                {uploadResult.data?.skillsAdded?.map((skill: string) => (
                  <span key={skill} className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-1 text-xs font-medium text-green-700 ring-1 ring-green-200">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Skills Already Exist */}
          {!uploadResult.data?.error && (uploadResult.data?.skillsAlreadyExist?.length ?? 0) > 0 && (
            <div className="rounded-lg bg-white/80 p-3 border border-blue-100">
              <p className="text-xs font-semibold text-gray-700 mb-2">
                Already in Your Profile
              </p>
              <div className="flex flex-wrap gap-2">
                {uploadResult.data?.skillsAlreadyExist?.map((skill: string) => (
                  <span key={skill} className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-600 ring-1 ring-gray-200">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={() => setUploadResult(null)}
            className={cn(
              "text-xs font-medium",
              uploadResult.data?.error ? "text-yellow-600 hover:text-yellow-700" : "text-blue-600 hover:text-blue-700"
            )}
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Upload Area */}
      {!selectedFile ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={cn(
            'relative flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-6 transition-colors',
            dragActive
              ? 'border-sky-500 bg-sky-50'
              : 'border-gray-300 hover:border-sky-500 hover:bg-gray-50'
          )}
        >
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleChange}
            className="absolute inset-0 cursor-pointer opacity-0"
            disabled={isUploading}
          />
          <Upload className="h-10 w-10 text-gray-400" />
          <p className="mt-3 text-sm font-medium text-gray-900 text-center">
            {hasResume ? 'Upload new resume' : 'Drop resume here'}
          </p>
          <p className="mt-1 text-xs text-gray-500 text-center">
            TXT format recommended for best AI extraction
          </p>
          <p className="mt-1 text-xs text-gray-400 text-center">
            Also supports PDF, DOCX (max 10MB)
          </p>
          {hasResume && (
            <p className="mt-2 text-xs text-blue-600 text-center">
              AI will extract skills automatically
            </p>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 p-3">
            <div className="flex items-center gap-2 flex-1 min-w-0">
              <FileText className="h-6 w-6 text-sky-600 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button
              onClick={() => setSelectedFile(null)}
              className="rounded-lg p-1.5 hover:bg-gray-200 flex-shrink-0"
              disabled={isUploading}
            >
              <X className="h-4 w-4 text-gray-500" />
            </button>
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="btn-primary w-full"
          >
            {isUploading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                Analyzing with AI...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <Sparkles className="h-4 w-4" />
                Upload & Extract Skills
              </span>
            )}
          </button>
        </div>
      )}

      {error && (
        <p className="mt-2 text-sm text-danger">{error}</p>
      )}
    </div>
  );
}
