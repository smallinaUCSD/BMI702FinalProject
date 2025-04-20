import React from 'react';

const TeamMember = ({ name, role, image, description }: { name: string, role: string, image: string, description: string }) => (
  <div className="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
    <img src={image} alt={name} className="w-full h-64 object-cover" />
    <div className="p-6">
      <h3 className="text-xl font-semibold mb-2">{name}</h3>
      <p className="text-blue-600 mb-4">{role}</p>
      <p className="text-gray-600">{description}</p>
    </div>
  </div>
);

const About = () => {
  const team = [
    {
      name: "Seshu Mallina",
      role: "DBMI Harvard Masters Student",
      image: "public/assets/seshu.jpg",
      description: "Seshu completed his undergraduate studies at UCSD, earning a degree in Bioinformatics and Computer Science. During his time at UCSD, he collaborated with Dr. Albert Leung to create a pipeline for analyzing brain MRIs for research studies. He also worked on various models to better understand patient demographics and classify brain diseases. Additionally, he interned at Infosys, where he built a machine learning model for Q&A tasks and contributed to improving stable diffusion models."
    },
    {
      name: "Rahul Gundamraj",
      role: "DBMI Harvard Masters Student",
      image: "public/assets/rahul.jpg",
      description: "Research Interests: Genome-Wide Association Studies, Drug Discovery, Next Generation Sequencing Analysis Previous Education:BS, Biomedical Engineering - University of Virginia"
    },
    {
      name: "Grant Bell",
      role: "DBMI Harvard Masters Student Advisor",
      image: "public/assets/grant.jpg",
      description: "Research Interests: Drug design, personalized medicine, machine learning, and neurodegenerative brain disease. Grant received his BS in Quantitative Biosciences and Engineering from the Colorado School of Mines. His research background includes small molecule synthesis for organic glass scintillatiors and developing machine learning models to study drug interactions to treat COVID-19. Grant is excited to unite his biochemistry background and computational training to advance drug design and personalized medicine. Previous Education:BS, Quantitative Biosciences and Engineering - Colorado School of Mines"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Meet Our Team</h1>
        <p className="text-xl text-gray-600">
          Dedicated professionals committed to transforming medical documentation
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {team.map((member, index) => (
          <TeamMember key={index} {...member} />
        ))}
      </div>
    </div>
  );
};

export default About;