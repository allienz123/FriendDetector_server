
#include "RecognizerI.h"

#include <fstream>

using namespace std;

char *recognize(char *);

Faces RecognizerI::findFacesAndRecognizePeople( const pair<const Byte*, const Byte*>&, const Current& )
{
	cout << "received request findFacesAndRecognizePeople" << endl;

	return vector<Face>();
}

Face RecognizerI::recognizeFace( const pair<const Byte*, const Byte*>& jpegFileOfFace, const Current& )
{
	ofstream ofp("temp.jpg");
	ofp.write((const char *)jpegFileOfFace.first, jpegFileOfFace.second - jpegFileOfFace.first);
	ofp.close();

	Face face;
	face.name = recognize("temp.jpg");
	
	return face;
}

void RecognizerI::learn( const pair<const Byte*, const Byte*>& jpegFileOfFace,
	   const string &name,	const Current& )
{
}

