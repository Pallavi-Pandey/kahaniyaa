import React, { useState, useEffect } from 'react';
import { Upload, Type, Users, Wand2, Languages, Volume2, Palette } from 'lucide-react';
import { storyAPI, ttsAPI, visionAPI, apiUtils, mockData } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const StoryCreator = ({ onStoryCreated }) => {
  const [inputType, setInputType] = useState('scenario');
  const [formData, setFormData] = useState({
    scenario: '',
    characters: [{ name: '', traits: '' }],
    setting: '',
    conflict: '',
    userDescription: '',
    language: 'en',
    tone: 'cheerful',
    targetAudience: 'kids',
    length: 500
  });
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [languages, setLanguages] = useState(mockData.languages);
  const [tones, setTones] = useState(mockData.tones);
  const [audiences, setAudiences] = useState(mockData.audiences);

  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    try {
      if (!apiUtils.mockMode) {
        const [languagesRes, tonesRes, audiencesRes] = await Promise.all([
          storyAPI.getSupportedLanguages(),
          storyAPI.getSupportedTones(),
          storyAPI.getTargetAudiences()
        ]);
        setLanguages(languagesRes.data.languages);
        setTones(tonesRes.data.tones);
        setAudiences(audiencesRes.data.audiences);
      }
    } catch (err) {
      console.error('Failed to load options:', err);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleCharacterChange = (index, field, value) => {
    const newCharacters = [...formData.characters];
    newCharacters[index][field] = value;
    setFormData(prev => ({ ...prev, characters: newCharacters }));
  };

  const addCharacter = () => {
    setFormData(prev => ({
      ...prev,
      characters: [...prev.characters, { name: '', traits: '' }]
    }));
  };

  const removeCharacter = (index) => {
    if (formData.characters.length > 1) {
      const newCharacters = formData.characters.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, characters: newCharacters }));
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const createStory = async () => {
    setLoading(true);
    setError('');

    try {
      let inputData = {};

      if (inputType === 'scenario') {
        inputData = { scenario: formData.scenario };
      } else if (inputType === 'image') {
        if (imageFile) {
          const uploadFormData = apiUtils.createFormData(imageFile, {
            user_description: formData.userDescription
          });
          const uploadRes = await visionAPI.uploadImage(uploadFormData);
          inputData = {
            user_description: formData.userDescription,
            image_url: uploadRes.data.image_url
          };
        } else {
          inputData = { user_description: formData.userDescription };
        }
      } else if (inputType === 'characters') {
        inputData = {
          characters: formData.characters.filter(char => char.name.trim()),
          setting: formData.setting,
          conflict: formData.conflict
        };
      }

      const storyRequest = {
        input_type: inputType,
        input_data: inputData,
        language: formData.language,
        tone: formData.tone,
        target_audience: formData.targetAudience,
        length: formData.length
      };

      const response = await storyAPI.createStory(storyRequest);
      onStoryCreated(response.data);
      
      // Reset form
      setFormData({
        scenario: '',
        characters: [{ name: '', traits: '' }],
        setting: '',
        conflict: '',
        userDescription: '',
        language: 'en',
        tone: 'cheerful',
        targetAudience: 'kids',
        length: 500
      });
      setImageFile(null);
      setImagePreview(null);
      
    } catch (err) {
      const errorInfo = apiUtils.handleError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  const renderScenarioInput = () => (
    <div className="space-y-4">
      <div className="form-group">
        <label className="form-label">Story Scenario</label>
        <textarea
          className="textarea"
          placeholder="Describe your story idea... (e.g., A brave little mouse goes on an adventure to find the magical cheese)"
          value={formData.scenario}
          onChange={(e) => handleInputChange('scenario', e.target.value)}
          rows={4}
        />
      </div>
    </div>
  );

  const renderImageInput = () => (
    <div className="space-y-4">
      <div className="form-group">
        <label className="form-label">Upload Image</label>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
            id="image-upload"
          />
          <label htmlFor="image-upload" className="cursor-pointer">
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">Click to upload an image</p>
            <p className="text-sm text-gray-400">PNG, JPG, GIF up to 10MB</p>
          </label>
        </div>
        {imagePreview && (
          <div className="mt-4">
            <img src={imagePreview} alt="Preview" className="max-w-full h-48 object-cover rounded-lg" />
          </div>
        )}
      </div>
      <div className="form-group">
        <label className="form-label">Additional Description (Optional)</label>
        <textarea
          className="textarea"
          placeholder="Add any additional context about the image..."
          value={formData.userDescription}
          onChange={(e) => handleInputChange('userDescription', e.target.value)}
          rows={3}
        />
      </div>
    </div>
  );

  const renderCharactersInput = () => (
    <div className="space-y-4">
      <div className="form-group">
        <label className="form-label">Characters</label>
        {formData.characters.map((character, index) => (
          <div key={index} className="flex space-x-2 mb-2">
            <input
              className="input flex-1"
              placeholder="Character name"
              value={character.name}
              onChange={(e) => handleCharacterChange(index, 'name', e.target.value)}
            />
            <input
              className="input flex-1"
              placeholder="Character traits"
              value={character.traits}
              onChange={(e) => handleCharacterChange(index, 'traits', e.target.value)}
            />
            {formData.characters.length > 1 && (
              <button
                type="button"
                onClick={() => removeCharacter(index)}
                className="btn btn-outline px-3"
              >
                ×
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          onClick={addCharacter}
          className="btn btn-outline text-sm"
        >
          + Add Character
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="form-group">
          <label className="form-label">Setting</label>
          <input
            className="input"
            placeholder="Where does the story take place?"
            value={formData.setting}
            onChange={(e) => handleInputChange('setting', e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="form-label">Conflict</label>
          <input
            className="input"
            placeholder="What challenge do they face?"
            value={formData.conflict}
            onChange={(e) => handleInputChange('conflict', e.target.value)}
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Create Your Story</h2>
        <p className="card-description">
          Choose how you'd like to create your story and customize the details
        </p>
      </div>
      
      <div className="card-content space-y-6">
        {/* Input Type Selection */}
        <div className="form-group">
          <label className="form-label">Story Input Type</label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { type: 'scenario', icon: Type, label: 'Text Scenario', desc: 'Describe your story idea' },
              { type: 'image', icon: Upload, label: 'Image Upload', desc: 'Upload an image for inspiration' },
              { type: 'characters', icon: Users, label: 'Characters', desc: 'Define characters and setting' }
            ].map(({ type, icon: Icon, label, desc }) => (
              <button
                key={type}
                onClick={() => setInputType(type)}
                className={`p-4 border-2 rounded-lg text-left transition-all ${
                  inputType === type
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <Icon className="h-6 w-6 mb-2 text-primary-500" />
                <h3 className="font-medium">{label}</h3>
                <p className="text-sm text-gray-500">{desc}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Input Content */}
        {inputType === 'scenario' && renderScenarioInput()}
        {inputType === 'image' && renderImageInput()}
        {inputType === 'characters' && renderCharactersInput()}

        {/* Story Configuration */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="form-group">
            <label className="form-label flex items-center space-x-2">
              <Languages className="h-4 w-4" />
              <span>Language</span>
            </label>
            <select
              className="input"
              value={formData.language}
              onChange={(e) => handleInputChange('language', e.target.value)}
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.native_name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label flex items-center space-x-2">
              <Palette className="h-4 w-4" />
              <span>Tone</span>
            </label>
            <select
              className="input"
              value={formData.tone}
              onChange={(e) => handleInputChange('tone', e.target.value)}
            >
              {tones.map(tone => (
                <option key={tone} value={tone}>
                  {tone.charAt(0).toUpperCase() + tone.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label flex items-center space-x-2">
              <Users className="h-4 w-4" />
              <span>Audience</span>
            </label>
            <select
              className="input"
              value={formData.targetAudience}
              onChange={(e) => handleInputChange('targetAudience', e.target.value)}
            >
              {audiences.map(audience => (
                <option key={audience} value={audience}>
                  {audience.charAt(0).toUpperCase() + audience.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Length (words)</label>
            <input
              type="number"
              className="input"
              min="100"
              max="1000"
              step="50"
              value={formData.length}
              onChange={(e) => handleInputChange('length', parseInt(e.target.value))}
            />
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        <button
          onClick={createStory}
          disabled={loading || !formData[inputType === 'scenario' ? 'scenario' : inputType === 'image' ? 'userDescription' : 'characters'].length}
          className="btn btn-primary w-full py-3 text-lg"
        >
          {loading ? (
            <LoadingSpinner size="sm" text="Creating your story..." />
          ) : (
            <>
              <Wand2 className="h-5 w-5 mr-2" />
              Create Story
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default StoryCreator;
