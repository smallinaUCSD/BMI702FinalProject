import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Clock, 
  Shield, 
  Sparkles 
} from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }: { icon: any, title: string, description: string }) => (
  <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300">
    <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full mb-4">
      <Icon className="h-6 w-6 text-blue-600" />
    </div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms for accurate medical text annotation"
    },
    {
      icon: Clock,
      title: "Real-time Processing",
      description: "Instant annotation results for efficient workflow"
    },
    {
      icon: Shield,
      title: "HIPAA Compliant",
      description: "Secure processing of sensitive medical information"
    },
    {
      icon: Sparkles,
      title: "Smart Highlighting",
      description: "Color-coded annotations for different medical entities"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Transform Medical Notes with Smart Annotations
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Streamline your medical documentation with AI-powered annotation tools
        </p>
        <Link
          to="/annotator"
          className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 transition-colors"
        >
          Try Annotator
        </Link>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((feature, index) => (
          <FeatureCard key={index} {...feature} />
        ))}
      </div>
    </div>
  );
};

export default Home;