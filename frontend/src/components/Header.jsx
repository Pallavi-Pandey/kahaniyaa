import React from 'react';
import { BookOpen, Sparkles, Globe } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8" />
              <Sparkles className="h-6 w-6 text-yellow-300" />
            </div>
            <div>
              <h1 className="text-3xl font-bold font-display">Kahaniyaa</h1>
              <p className="text-primary-100 text-sm">Multilingual Storytelling Platform</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-primary-100">
              <Globe className="h-5 w-5" />
              <span className="text-sm">English • हिन्दी • தமிழ்</span>
            </div>
          </div>
        </div>
        
        <div className="mt-4">
          <p className="text-primary-100 text-lg">
            Create magical stories with AI-powered narration in multiple languages
          </p>
        </div>
      </div>
    </header>
  );
};

export default Header;
