use HTTP::Daemon;
use HTTP::Status; 
use HTTP::Response;

#use IO::File;

my $d = HTTP::Daemon->new(
         LocalAddr => 'localhost',
         LocalPort => 8001,
     )|| die;

print "Please contact me at: <URL:", $d->url, ">\n";


while (my $c = $d->accept) {
    while (my $r = $c->get_request) {
        if ($r->method eq 'GET') {
            
            $file_s= "./index.html";    # index.html - jakis istniejacy plik
            $c->send_file_response($file_s);

        }
        elsif($r->method eq 'POST')
        {
            print $r->as_string, "\n";
        my $response = HTTP::Response->new(200);
        $response->header("Content-Type" => "text/text");
        $response->content($r->as_string);
        $c->send_response($response);
        }
        else {
            $c->send_error(RC_FORBIDDEN)
        }

    }
    $c->close;
    undef($c);
}